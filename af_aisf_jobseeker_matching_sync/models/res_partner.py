
import logging
import time
import traceback
from psycopg2 import IntegrityError, InternalError
from uuid import uuid4
import odoo
from odoo import models, api, registry

_logger = logging.getLogger(__name__)

RASK_SYNC = "RASK SYNC"
MASK_SYNC = "MASK SYNC"


class Arbetssokande(models.Model):
    _inherit = "arbetssokande"

    @api.model
    def _aisf_sync_jobseeker_matching(
        self,
        db_values,
        process_name,
        customer_id,
        social_sec_nr=False,
        eventid=None,
        batch=None,
    ):
        """Perform a sync of a jobseeker from AIS-F.
        :param customer_id: Customer ID of the jobseeker.
        :param social_sec_nr: Optional social security number of the jobseeker.
        :param eventid: The MQ message id for logging purposes.
        :returns: True if sync succeeded.
        """
        log = self.env["af.process.log"]
        if not batch:
            log.log_message(process_name, eventid, "SYNC STARTED", objectid=customer_id)

        partner = self.env["arbetssokande"].search(
            [("customer_id", "=", customer_id)]
        )
        if not partner and social_sec_nr:
            partner = self.env["arbetssokande"].search_pnr(social_sec_nr)
        eventid = eventid or uuid4()

        mask_matching = self.env.ref("af_ipf.ipf_endpoint_mask_matching").sudo()
        try:
            if not batch:
                log.log_message(process_name, eventid, MASK_SYNC, objectid=customer_id)
            start_time = time.time()
            res = mask_matching.call(customer_id=int(customer_id))
            end_time = time.time()
            time_for_call_to_mask_matching = end_time - start_time
        except Exception:
            em = traceback.format_exc()
            log.log_message(
                process_name,
                eventid,
                MASK_SYNC,
                objectid=customer_id,
                error_message=em,
                status=False,
            )
            return
        if not res:
            log.log_message(
                process_name,
                eventid,
                MASK_SYNC,
                objectid=customer_id,
                error_message="NOT IN AIS-F",
                status=False,
                info_1=time_for_call_to_mask_matching,
            )
            return

        try:


            # "kompl_matchning_info": res.get("komplMatchningInfo"), # ovrig_erfarenhet, not implemented

            # arbetssokande.yrke.yrke_id on both and what even is that?
            # "ssyk_kompetensutveckling": res.get("ssykKompetensutveckling"),
            # "yrke_kompetensutveckling": res.get("yrkeKompetensutveckling"),

            # yrke.yrkesgrupp_id on both and once again what even is that?
            # "onskat_yrke_ssyk": res.get("onskatYrkeSsyk"),
            # "onskat_yrke": res.get("onskatYrke"),

            # arbetssokande.yrke.validering_onskat_yrke once again none of this makes any sense to me
            # "validering_onskat_yrke": res.get("valideringOnskatYrke"),

            varaktighet_fran = res.get("varaktighetFran"),
            varaktighet_till = res.get("varaktighetTill"),
            varaktighet_fran_id = self.env['vf.varaktighet'].search([('concept_id', '=', varaktighet_fran)]).id
            varaktighet_till_id = self.env['vf.arbetstid'].search([('concept_id', '=', varaktighet_till)]).id
            arbetstid = res.get("arbetstid")
            arbetstid_id = self.env['vf.arbetstid'].search([('concept_id', '=', arbetstid)]).id

            onskade_anstallningsvillkor_dict = {
                "arbetstid_id": arbetstid_id,
                "varaktighet_fran": varaktighet_fran_id,
                "varaktighet_till": varaktighet_till_id,
                "arbetstid_beskrivning": res.get("arbetstidBeskrivning"),
                "meriter_uppdat_datum": res.get("meriterUppdatDatum"),
                "flytta_veckopendla": res.get("flyttaVeckopendla"),
                "soker_inom_eu": res.get("sokerInomEu"),
                "kan_ej_valja_yrke": res.get("kanEjValjaYrke"),
                "kan_ej_ta_tidigare_yrke": res.get("kanEjTaTidigareYrke"),
            }
            onskade_anstallningsvillkor_id = self.env[
                'arbetssokande.onskade_anstallningsvillkor'].create(
                onskade_anstallningsvillkor_dict).id

            arbetssokande_dict = {
                # "meriter_finns": res.get("meriterFinns"), # not implemented
                # "matchningsbar": res.get("matchningsbar"), # not implemented
                "onskade_anstallningsvillkor_id": onskade_anstallningsvillkor_id

            }
            arbetssokande_id = self.env['arbetssokande'].create(arbetssokande_dict)

            for yrke in res.get("yrkenAttSoka"):
                yrke_dict = {
                    "yrke_id": self.env['vf.ssyk'].search([('concept_id', '=', yrke.get("yrke"))]),
                    "utbildning": yrke.get("utbildning"),
                    "erfarenhet": yrke.get("erfarenhet"),
                    "arbetssokande_id": arbetssokande_id
                }
                self.env['arbetssokande.yrke'].create(yrke_dict).id

            for sprak in res.get("sprak"):
                sprak_id = self.env["vf.sprak"].search([('concept_id', '=', sprak.get("konceptId"))])
                self.env['arbetssokande.sprakkunskap'].create({
                    'sprak_id': sprak_id,
                    'arbetssokande_id': arbetssokande_id
                })

            for kompetensord in res.get("kompetensord"):
                kompetensord_id = self.env["vf.kompetensord"].search([
                    (
                        'concept_id',
                        '=',
                        kompetensord.get("konceptId")
                    )])
                self.env['arbetssokande.kompetensord'].create({
                    'kompetensord_id': kompetensord_id,
                    'arbetssokande_id': arbetssokande_id
                })

            for sokt_omrade in res.get("soktaOmraden"):
                lan_id = self.env["vf.region"].search([('concept_id', '=', sokt_omrade)])
                self.env['arbetssokande.geografiskt_sokomrade'].create({
                    'lan_id': lan_id,
                    'arbetssokande_id': arbetssokande_id
                })

            for korkort in res.get("korkort"):
                korkort_id = self.env["vf.korkortsbehorighet"].search([('concept_id', '=', korkort)])
                self.env['arbetssokande.korkortsklass'].create({
                    "korkort_id": korkort_id,
                    "tillgang_bil": res.get("tillgangBil"),
                    "arbetssokande_id": arbetssokande_id
                })



            # not implemented
            for sokord in res.get("sokord"):
                matchningsord_dict = {
                    "benamning": sokord.get("benamning"),
                    "nyckel": sokord.get("nyckel"),
                }

        except Exception:
            em = traceback.format_exc()
            log.log_message(
                process_name,
                eventid,
                MASK_SYNC,
                objectid=customer_id,
                error_message=em,
                status=False,
            )
            return

        log.log_message(
            process_name,
            eventid,
            "SYNC COMPLETED",
            objectid=customer_id,
            info_1=time_for_call_to_mask_matching,
            info_2=create_update,
        )

        return True

    @classmethod
    def _try_unlink_class(cls, partner_id, cr, uid):
        with api.Environment.manage():
            res = None
            env_unlink = api.Environment(cr, uid, {})[cls._name]
            try:
                # try to delete the partner.
                env_unlink._try_unlink(partner_id, cr, uid)
            except IntegrityError as e:
                # mark partner as SPU and remove all sensitive information.
                partner = env_unlink.browse(partner_id)
                anon_partner = {
                    "is_spu": True,
                    "name": "ANONYMIZED",
                    "social_sec_nr": False,
                    "email": False,
                    "mobile": False,
                    "phone": False,
                    "education_ids": [(5, 0, 0)],
                }
                child_list = []
                for child in partner.child_ids:
                    child_list.append((2, child.id, 0))
                anon_partner["child_ids"] = child_list
                partner.write(anon_partner)

                # dump error to log so we can monitor it in kibana.
                _logger.warning(e)
                res = e
            finally:
                cr.commit()
            return res

    @api.model
    def _try_unlink(self, partner_id, cr, uid):
        try:
            if self.pool != self.pool.check_signaling():
                # the registry has changed, reload self in the new registry
                self.env.reset()
                self = self.env()[self._name]
            self.env["arbetssokande"].browse(partner_id).unlink()
            self.env["arbetssokande"].invalidate_cache()
            self.pool.signal_changes()
        except IntegrityError as e:
            self.pool.reset_changes()
            cr.rollback()
            raise e
