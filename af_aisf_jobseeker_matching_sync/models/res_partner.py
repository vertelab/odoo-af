
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


class Partner(models.Model):
    _inherit = "res.partner"

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

        partner = self.env["res.partner"].search(
            [("customer_id", "=", customer_id), ("is_jobseeker", "=", True)]
        )
        if not partner and social_sec_nr:
            partner = self.env["res.partner"].search_pnr(social_sec_nr)
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
            {
                "arbetstid": res.get("arbetstid"),
                "arbetstid_beskrivning": res.get("arbetstidBeskrivning"),
                "meriter_finns": res.get("meriterFinns"),
                "meriter_uppdat_datum": res.get("meriterUppdatDatum"),
                "flytta_veckopendla": res.get("flyttaVeckopendla"),
                "soker_inom_eu": res.get("sokerInomEu"),
                "matchningsbar": res.get("matchningsbar"),
                "kompl_matchning_info": res.get("komplMatchningInfo"),
                "korkort": res.get("korkort"),
                "tillgang_bil": res.get("tillgangBil"),
                "ssyk_kompetensutveckling": res.get("ssykKompetensutveckling"),
                "yrke_id_kompetensutveckling": res.get("yrkeIdKompetensutveckling"),
                "onskat_yrke_ssyk": res.get("onskatYrkeSsyk"),
                "onskat_yrke_id": res.get("onskatYrkeId"),
                "validering_onskat_yrke": res.get("valideringOnskatYrke"),
                "varaktighet1": res.get("varaktighet1"),
                "varaktighet2": res.get("varaktighet2"),
            }
            for yrke in res.get("soktaYrken"):
                yrke_dict = {
                    "yrke_id": yrke.get("yrkeId"),
                    "ssyk": yrke.get("ssyk"),
                    "utbildning": yrke.get("utbildning"),
                    "erfarenhet": yrke.get("erfarenhet")
                }
            for matchningsord in res.get("matchningsord"):
                matchningsord_dict = {
                    "taxonomyId": matchningsord.get("taxonomyId"),
                    "matchningsord": matchningsord.get("matchningsord"),
                    "typ": matchningsord.get("typ")
                }

            mask_keys = {
                "arbetstid": "HELTID",
                "arbetstidBeskrivning": "string",
                "meriterFinns": "true",
                "meriterUppdatDatum": "2020-07-22T08:39:27.300Z",
                "flyttaVeckopendla": "true",
                "sokerInomEu": "true",
                "matchningsbar": "true",
                "komplMatchningInfo": "string",
                "korkort": "string",
                "tillgangBil": "true",
                "ssykKompetensutveckling": "string",
                "yrkeIdKompetensutveckling": 0,
                "onskatYrkeSsyk": "string",
                "onskatYrkeId": 0,
                "valideringOnskatYrke": "BEHOV_AV_FORDJUPAD_KOMPETENSKARTLAGGNING",
                "varaktighet1": "ODEFINERAD",
                "varaktighet2": "ODEFINERAD",
                "soktaYrken": [
                    {
                        "yrkeId": 0,
                        "ssyk": "string",
                        "utbildning": "true",
                        "erfarenhet": "true"
                    }
                ],
                "soktaKommuner": [
                    "string"
                ],
                "matchningsord": [
                    {
                        "taxonomyId": 0,
                        "matchningsord": "string",
                        "typ": "string"
                    }
                ]
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
            self.env["res.partner"].browse(partner_id).unlink()
            self.env["res.partner"].invalidate_cache()
            self.pool.signal_changes()
        except IntegrityError as e:
            self.pool.reset_changes()
            cr.rollback()
            raise e
