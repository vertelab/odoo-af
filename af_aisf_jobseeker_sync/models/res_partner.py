from odoo import models, api, registry
import odoo
from uuid import uuid4
from psycopg2 import IntegrityError, InternalError
import traceback
import time
import logging

_logger = logging.getLogger(__name__)

RASK_SYNC = "RASK SYNC"
MASK_SYNC = "MASK SYNC"


class Partner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _aisf_sync_jobseeker(
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
        eventid = eventid or uuid4()
        log = self.env["af.process.log"]
        if not batch:
            log.log_message(process_name, eventid, "SYNC STARTED", objectid=customer_id)

        partner = self.env["res.partner"].search(
            [("customer_id", "=", customer_id), ("is_jobseeker", "=", True)]
        )
        if not partner and social_sec_nr:
            partner = self.env["res.partner"].search_pnr(social_sec_nr)

        rask = self.env.ref("af_ipf.ipf_endpoint_rask").sudo()
        try:
            if not batch:
                log.log_message(process_name, eventid, RASK_SYNC, objectid=customer_id)
            start_time = time.time()
            res = rask.call(customer_id=int(customer_id))
            end_time = time.time()
            time_for_call_to_rask = end_time - start_time
        except Exception:
            em = traceback.format_exc()
            log.log_message(
                process_name,
                eventid,
                RASK_SYNC,
                objectid=customer_id,
                error_message=em,
                status=False,
            )
            return
        if not res:
            log.log_message(
                process_name,
                eventid,
                RASK_SYNC,
                objectid=customer_id,
                error_message="NOT IN AIS-F",
                status=False,
                info_1=time_for_call_to_rask,
            )
            return
        customer_id = res.get("arbetssokande", {}).get("sokandeId")

        if res.get("processStatus", {}).get("skyddadePersonUppgifter"):
            # jobseeker has SPU status. partner should be removed
            if partner:
                # cancel all meetings with this jobseeker
                cancel_reason = self.env.ref(
                    "calendar_af.reason_authority", raise_if_not_found=False
                )
                # if we didn't find the cancel_reason we do not have
                # calendar_af module installed and there's no need to
                # continue with canceling meetings. It would crash.
                if cancel_reason and hasattr(partner, 'appointment_ids'):
                    partner.appointment_ids._cancel(cancel_reason)
                # Use special method _try_unlink_class to unlink this partner.
                # This is done in order to avoid psql locking our cursor if
                # we run into a problem while unlinking.
                partner_id = partner.id
                dbname = self.env.cr.dbname
                db = odoo.sql_db.db_connect(dbname)
                cr_unlink = db.cursor()
                reg_unlink = odoo.registry(dbname)[self._name]
                res_unlink = reg_unlink._try_unlink_class(
                    partner_id, cr_unlink, self.env.uid
                )
                if not res_unlink:
                    # partner was unlinked
                    log.log_message(
                        process_name,
                        eventid,
                        RASK_SYNC,
                        objectid=customer_id,
                        error_message="SPU",
                        info_1=time_for_call_to_rask,
                        info_2="delete",
                    )
                else:
                    # partner could not be unlinked
                    log.log_message(
                        process_name,
                        eventid,
                        RASK_SYNC,
                        objectid=customer_id,
                        error_message="SPU",
                        info_1=time_for_call_to_rask,
                        info_2=res_unlink,
                    )
                cr_unlink.close()
            else:
                log.log_message(
                    process_name,
                    eventid,
                    RASK_SYNC,
                    objectid=customer_id,
                    error_message="SPU",
                    info_1=time_for_call_to_rask,
                    info_2="not created",
                )
            return True

        try:
            state = res.get("kontaktuppgifter", {}).get("hemkommunKod")
            # TODO: Would probably be best to add country here? I believe
            #  code is unique per country.
            if not db_values:
                state = state and self.env["res.country.state"].search_read(
                    [("code", "=", state)], ["id"], limit=1
                )
                state = state and state[0]["id"] or None
            else:
                state = db_values["res.country.state"].get(state, False)

            office = res.get("kontor", {}).get("kontorsKod")
            if not db_values:
                office = office and self.env["hr.department"].search_read(
                    [("office_code", "=", office)], ["id"], limit=1
                )
                office = office and office[0]["id"] or None
            else:
                office = db_values["hr.department"].get(office, False)

            sun = res.get("utbildning", {}).get("sunKod")
            if not db_values:
                sun = sun and self.env["res.sun"].search([("code", "=", sun)])
                sun = sun or self.env["res.sun"].search([("code", "=", "999")]) or False
                if sun:
                    sun = sun["id"]
            else:
                sun = db_values["res.sun"].get(sun, db_values["res.sun"].get("999"))

            skat = res.get("kontakt", {}).get("sokandekategoriKod")
            if not db_values:
                skat = skat and self.env["res.partner.skat"].search_read(
                    [("code", "=", skat)], ["id"], limit=1
                )
                skat = skat and skat[0]["id"] or None
            else:
                skat = db_values["res.partner.skat"].get(skat, False)

            user = res.get("kontor", {}).get("ansvarigHandlaggareSignatur")
            if not db_values:
                user = user and self.env["res.users"].search_read(
                    [("login", "=", user)], ["id"], limit=1
                )
                user = user and user[0]["id"] or None
            else:
                user = db_values["res.users"].get(user, False)

            segmenteringsval = res.get("segmentering", {}).get("segmenteringsval")
            if segmenteringsval == "LOKAL":
                registered_through = "local office"
            elif segmenteringsval == "SJALVSERVICE":
                registered_through = "self service"
            elif segmenteringsval == "PDM":
                registered_through = "pdm"
            else:
                registered_through = False

            if res.get("medgivande", {}).get("infoTillArbetsgivare"):
                share_info_with_employers = "True"
            else:
                share_info_with_employers = "False"

            if res.get("medgivande", {}).get("paminnelseViaSms"):
                sms_reminders = "True"
            else:
                sms_reminders = "False"
            education_level = res.get("utbildning", {}).get("utbildningsniva")
            if education_level is not None:
                try:
                    if not db_values:
                        education_level = self.env[
                            "res.partner.education.education_level"
                        ].search([("name", "=", int(education_level))])
                        if education_level:
                            education_level = education_level.id
                    else:
                        education_level = db_values["education_level"].get(
                            int(education_level), False
                        )
                except ValueError:
                    education_level = False
            else:
                education_level = False

            last_contact_type = res.get("kontakt", {}).get("senasteKontakttyp") or False
            if last_contact_type:
                last_contact_type = last_contact_type[0]

            next_contact_type = (
                res.get("kontakt", {}).get("nastaKontakttyper", {}) or False
            )
            if next_contact_type:
                list_next_contact_type = [w[0] for w in next_contact_type]
                next_contact_type = ''.join(list_next_contact_type)
            jobseeker_dict = {
                "firstname": res.get("arbetssokande", {}).get(
                    "fornamn", "MISSING FIRSTNAME"
                ),
                "lastname": res.get("arbetssokande", {}).get(
                    "efternamn", "MISSING LASTNAME"
                ),
                "customer_id": customer_id,
                "social_sec_nr": res.get("arbetssokande", {}).get("personnummer"),
                "customer_since": res.get("processStatus", {}).get("aktuellSedanDatum"),
                "share_info_with_employers": share_info_with_employers,
                "phone": res.get("kontaktuppgifter", {}).get("telefonBostad"),
                "work_phone": res.get("kontaktuppgifter", {}).get("telefonArbetet"),
                "mobile": res.get("kontaktuppgifter", {}).get("telefonMobil"),
                "jobseeker_category_id": skat,
                "deactualization_date": res.get("processStatus", {}).get(
                    "avaktualiseringsDatum"
                ),
                "deactualization_reason": res.get("processStatus", {}).get(
                    "avaktualiseringsOrsaksKod"
                ),
                "email": res.get("kontaktuppgifter", {}).get("epost"),
                "office_id": office,
                "state_id": state,
                "registered_through": registered_through,
                "user_id": user,
                "sms_reminders": sms_reminders,
                "next_contact_date": res.get("kontakt", {}).get("nastaKontaktdatum"),
                "next_contact_time": res.get("kontakt", {}).get("nastaKontaktTid"),
                "next_contact_type": next_contact_type,
                "last_contact_date": res.get("kontakt", {}).get("senasteKontaktdatum"),
                "last_contact_type": last_contact_type,
                "is_jobseeker": True,
            }

            if sun and education_level:
                if partner:
                    edu_filtered = partner.education_ids.filtered(
                        lambda e: (e.sun_id and e.sun_id.id == sun)
                        and (
                            e.education_level_id
                            and e.education_level_id.id == education_level
                        )
                    )
                    if edu_filtered:
                        # Already exists. Do nothing.
                        pass
                    else:
                        # delete education with source from AIS-F
                        aisf_edu = partner.education_ids.filtered(lambda e: e.is_rask)
                        if aisf_edu:
                            aisf_edu.unlink()
                        # add empty list to jobseeker_dict to trigger next if
                        jobseeker_dict["education_ids"] = []
                else:
                    jobseeker_dict["education_ids"] = []
                if "education_ids" in jobseeker_dict:
                    jobseeker_dict["education_ids"].append(
                        (
                            0,
                            0,
                            {
                                "sun_id": sun,
                                "education_level_id": education_level,
                                "is_rask": True,
                            },
                        )
                    )

            if partner:
                partner.with_context(tracking_disable=True).write(jobseeker_dict)
                create_update = "update"
            else:
                partner = (
                    self.env["res.partner"]
                    .with_context(tracking_disable=True, install_mode=True)
                    .create(jobseeker_dict)
                )
                create_update = "create"

            own_or_foreign_address_given = False
            for address in res.get("kontaktuppgifter", {}).get("adresser", {}):
                streetaddress = address.get("gatuadress")
                if streetaddress:
                    streetadress_array = streetaddress.split(",")
                    if len(streetadress_array) == 1:
                        street = streetadress_array[0]
                        street2 = False
                    elif len(streetadress_array) > 1:
                        street = streetadress_array[1]
                        street2 = streetadress_array[0]
                    co_address = address.get("coAdress")
                    zip = address.get("postnummer")
                    city = address.get("postort")
                    country = address.get("landsadress")
                    if country:
                        if not db_values:
                            country = (
                                self.env["res.country"]
                                .with_context(lang="sv_SE")
                                .search([("name", "ilike", country)])
                            )
                            country = country["id"] or None
                        else:
                            country = db_values["res.country"].get(country, False)
                    if address.get("adressTyp") == "FBF":
                        partner.address_co = co_address
                        partner.street = street
                        partner.street2 = street2
                        partner.zip = zip
                        partner.city = city
                        partner.country_id = country
                    elif (
                        address.get("adressTyp") == "EGEN"
                        or address.get("adressTyp") == "UTL"
                    ):
                        own_or_foreign_address_given = True
                        given_address_object = self.env["res.partner"].search(
                            [("parent_id", "=", partner.id)]
                        )
                        if not given_address_object:
                            given_address_dict = {
                                "address_co": co_address,
                                "parent_id": partner.id,
                                "street": street,
                                "street2": street2,
                                "zip": zip,
                                "city": city,
                                "type": "given address",
                                "country_id": country,
                            }
                            self.env["res.partner"].create(given_address_dict)
                        else:
                            given_address_object.address_co = co_address
                            given_address_object.street = street
                            given_address_object.street2 = street2
                            given_address_object.zip = zip
                            given_address_object.city = city
                            given_address_object.country_id = country
            if not own_or_foreign_address_given:
                given_address_object = self.env["res.partner"].search(
                    [("parent_id", "=", partner.id)]
                )
                if given_address_object:
                    given_address_object.unlink()

            utbildningsplikt_kod_id = self.env['arbetssokande.vf.' \
                                               'utbildningsplikt'].search(
                [
                    ('code', '=', res.get("utbildning", {}).get("utbildningspliktKod"))
                ]
            ).id
            intensivar_id = self.env['arbetssokande.vf.intensivar'].search(
                [
                    ('description', '=', res.get("intensivar", {}).get("status"))
                ]
            ).id
            fordjupad_samverkan_insatstyps_kod_id = self.env['arbetssokande.vf.' \
                                                             'insatstyp_kod'].search(
                [
                    ('code', '=', res.get("fordjupadSamverkan", {}).get("insatstypsKod"))
                ]
            ).id
            antal_forbr_akassadagar_id = self.env['arbetssokande.vf.' \
                                                  'antal_forbr_akassadagar'].search(
                [
                    ("code",
                     "=",
                     res.get("akassa", {}).get("antalForbrAkassadagar")
                     )
                ]
            ).id
            akassa_kod_id = self.env['arbetssokande.vf.' \
                                     'akassa_kod'].search(
                [
                    ("code",
                     "=",
                     res.get("akassa", {}).get("akassaKod")
                     )
                ]
            ).id
            if res.get("etablering", {}).get("tillhorEtablering2010"):
                tillhor_etablering = "2010"
            elif res.get("etablering", {}).get("tillhorEtablering2017"):
                tillhor_etablering = "2017"
            else:
                tillhor_etablering = False

            arbetssokande_dict = {
                'partner_id': partner.id,
                "fodelsedatum": res.get("arbetssokande", {}).get("fodelsedatum"),
                "uppdat_vecka_akassadagar": res.get("akassa", {}).get(
                    "uppdatVeckaAkassadagar"
                ),
                "akasse_status": res.get("akassa", {}).get("akasseStatus"),
                "af_akasse_status": res.get("akassa", {}).get("afAkasseStatus"),
                "utrikesfodd": res.get("etablering", {}).get("utrikesfodd"),
                "etableringssamtal_datum": res.get("etablering", {}).get("etableringssamtalDatum"),
                "fordjupad_samverkan_startdatum": res.get("fordjupadSamverkan", {}).get("startdatum"),
                "fordjupad_samverkan_slutdatum": res.get("fordjupadSamverkan", {}).get("slutdatum"),
                "avslutsorsaks_kod": res.get("fordjupadSamverkan", {}).get("avslutsorsaksKod"),
                "sokandekategori_sedan": res.get("kontakt", {}).get("sokandekategoriSedan"),
                "kontor_sektionskod": res.get("kontor", {}).get("sektionsKod"),
                "info_till_arbetsgivare_via_epost": res.get("medgivande", {}).get("infoTillArbetsgivareViaEpost"),
                "beraknad_sysselsattnings_datum": res.get("processStatus", {}).get("beraknadSysselsattningsDatum"),
                "accepterar_automatisk_utskrivning": res.get("processStatus", {}).get("accepterarAutomatiskUtskrivning"),
                "skatteverket_sekretessmarkering": res.get("processStatus", {}).get("skatteverketSekretessmarkering"),
                "skatteverket_skyddad_folkbokforing": res.get("processStatus", {}).get("skatteverketSkyddadFolkbokforing"),
                "spar_status": res.get("processStatus", {}).get("sparStatus"),
                "lagrad": res.get("processStatus", {}).get("lagrad"),
                "sjalvinskriven": res.get("processStatus", {}).get("sjalvinskriven"),
                "fastTillaggskodAF1": res.get("tillaggskod", {}).get("fastTillaggskodAF1"),
                "fastTillaggskodAF2": res.get("tillaggskod", {}).get("fastTillaggskodAF2"),
                "fastTillaggskodKontor": res.get("tillaggskod", {}).get("fastTillaggskodKontor"),
                "tillfTillaggskodKontor": res.get("tillaggskod", {}).get("tillfTillaggskodKontor"),
                "tillhor_etablering": tillhor_etablering,
                "akassa_kod_id": akassa_kod_id,
                "antal_forbr_akassadagar_id": antal_forbr_akassadagar_id,
                "fordjupad_samverkan_insatstyps_kod_id": fordjupad_samverkan_insatstyps_kod_id,
                "intensivar_id": intensivar_id,
                "utbildningsplikt_kod_id": utbildningsplikt_kod_id
            }
            arbetssokande_id = self.env['arbetssokande'].create(arbetssokande_dict)

            for akassa_period in res.get("akassa", {}).get("akassaperioder", []):
                akasseperiod_dict = {
                    'start_datum': akassa_period.get("startdatum"),
                    'slut_datum': akassa_period.get("slutdatum"),
                    'arbetssokande_id': arbetssokande_id
                }
                self.env['arbetssokande.akassaperiod'].create(akasseperiod_dict)

            for funktionsnedsattning in res.get("funktionsnedsattning", {}).get(
                    "funktionsnedsattningar"):
                funktionsnedsattning_dict = {
                    'funktionsnedsattning_id': self.env['arbetssokande.vf.' \
                                                        'funktionsnedsattning'].search(
                        [
                            (
                                "code",
                                "=",
                                funktionsnedsattning.get("kod")
                            )
                        ]
                    ).id,
                    'arbetssokande_id': arbetssokande_id
                }
                self.env['arbetssokande.funktionsnedsattning'].create(
                    funktionsnedsattning_dict)

            for overhoppningsbar_tid in res.get("overhoppningsbarTid", {}).get(
                    "overhoppningsbaraTider"):
                overhoppningsbar_tid_dict = {
                    'overhoppningsbar_tid_typ_id': self.env['arbetssokande.vf.' \
                                                            'overhoppningsbar_tid'].search(
                        [
                            (
                                "description",
                                "=",
                                overhoppningsbar_tid.get("typ")
                            )
                        ]
                    ).id,
                    'arbetssokande_id': arbetssokande_id,
                    'start_datum': overhoppningsbar_tid.get("startdatum"),
                    'slut_datum': overhoppningsbar_tid.get("slutdatum"),
                }
                self.env['arbetssokande.overhoppningsbar_tid'].create(
                    overhoppningsbar_tid_dict)

            for office_code in res.get("kontor", {}).get(
                    "ekonomisktBeslutVidAndraKontorsKoder"):
                ekonomiskt_beslut_vid_andra_kontors_koder_dict = {
                    'arbetssokande_id': arbetssokande_id,
                    'kontors_id': self.env['hr.department'].search([
                        ('office_code', '=', office_code)
                    ]).id,
                }
                self.env['arbetssokande.ekonomiskt_beslut_vid_andra_kontors_kod'].create(
                    ekonomiskt_beslut_vid_andra_kontors_koder_dict)

            remaining_keys_dict = {
                "funktionsnedsattning": {
                    "ungMedFunktionsnedsattning": "false",
                },
                "kontakt": {
                    "tolksprak": "en",
                    "tolkleveranssatt": "Expresstolk"
                },
                "personnummerbyte": {
                    "personnummerbyteBestallt": "false",
                    "personnummerbyten": [
                        {
                            "bytesdatum": "2015-01-01",
                            "tidigarePersonnummer": 199304162390
                        }
                    ]
                },
                "rehabSamverkan": {
                    "malgruppsKod": "1",
                    "startdatum": "2017-01-01",
                    "slutdatum": "2017-01-01",
                    "avslutsorsaksKod": "2"
                },
                "tidigInsats": {
                    "status": "BEHOV_FINNS",
                    "startdatum": "2018-11-23",
                    "slutdatum": "2019-11-23"
                },
                "tillaggsdag": {
                    "tillaggsdagar": [
                        {
                            "startdatum": "2015-01-01",
                            "slutdatum": "2015-01-05",
                            "antaldagar": 4,
                            "Raderad": "true"
                        }
                    ]
                },
            }

        except Exception:
            em = traceback.format_exc()
            log.log_message(
                process_name,
                eventid,
                RASK_SYNC,
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
            info_1=time_for_call_to_rask,
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
