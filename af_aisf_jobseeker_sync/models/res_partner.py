#  Copyright (c) 2021 Arbetsförmedlingen.

from odoo import models, api
from uuid import uuid4
import traceback

import logging

_logger = logging.getLogger(__name__)

RASK_SYNC = "RASK SYNC"
MASK_SYNC = "MASK SYNC"

class Partner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _aisf_sync_jobseeker(self, process_name, customer_id, eventid=None):
        """ Perform a sync of a jobseeker from AIS-F.
        :param customer_id: Customer ID of the jobseeker.
        :param eventid: The MQ message id for logging purposes.
        :returns: True if sync succeeded.
        """
        log = self.env['af.process.log']
        log.log_message(process_name, eventid, "SYNC STARTED", objectid=customer_id)

        partner = self.env['res.partner'].search(
            [('customer_id', '=', customer_id), ('is_jobseeker', '=', True)])
        eventid = eventid or uuid4()

        rask = self.env.ref('af_ipf.ipf_endpoint_rask').sudo()
        try:
            log.log_message(process_name, eventid, RASK_SYNC, objectid=customer_id)
            res = rask.call(customer_id=int(customer_id))
        except Exception:
            em = traceback.format_exc()
            log.log_message(process_name, eventid, RASK_SYNC,
                            objectid=customer_id, error_message=em, status=False)
            return
        if not res:
            log.log_message(process_name, eventid, RASK_SYNC,
                            objectid=customer_id, error_message="NOT IN AIS-F", status=False)
            return
        customer_id = res.get('arbetssokande', {}).get('sokandeId')
        if res.get('processStatus', {}).get('skyddadePersonUppgifter'):
            log.log_message(process_name, eventid, RASK_SYNC,
                            objectid=customer_id, error_message="SUP")
            return True
        try:
            state = res.get('kontaktuppgifter', {}).get('hemkommunKod')
            # TODO: Would probably be best to add country here? I believe
            #  code is unique per country.
            state = state and self.env['res.country.state'].search([('code', '=', state)])

            office = res.get('kontor', {}).get('kontorsKod')
            office = office and self.env['hr.department'].search([('office_code', '=', office)])

            sun = res.get('utbildning', {}).get('sunKod')
            sun = sun and self.env['res.sun'].search([('code', '=', sun)])
            sun = sun or self.env['res.sun'].search([('code', '=', '999')]) or False

            skat = res.get('kontakt', {}).get('sokandekategoriKod')
            skat = skat and self.env['res.partner.skat'].search([('code', '=', skat)])

            user = res.get('kontor', {}).get('ansvarigHandlaggareSignatur')
            user = user and self.env['res.users'].search([('login', '=', user)])

            segmenteringsval = res.get('segmentering', {}).get('segmenteringsval')
            if segmenteringsval == "LOKAL":
                registered_through = "local office"
            elif segmenteringsval == "SJALVSERVICE":
                registered_through = "self service"
            elif segmenteringsval == "PDM":
                registered_through = "pdm"
            else:
                registered_through = False

            education_level = res.get('utbildning', {}).get('utbildningsniva')
            if education_level is not None:
                try:
                    education_level = self.env['res.partner.education.education_level'].search(
                        [('name', '=', int(education_level))])
                except ValueError:
                    education_level = False
            else:
                education_level = False

            last_contact_type = res.get('kontakt', {}).get('senasteKontakttyp') or False
            if last_contact_type:
                last_contact_type = last_contact_type[0]

            next_contact_type = res.get('kontakt', {}).get('nastaKontakttyper', {}) or False
            if next_contact_type:
                next_contact_type = next_contact_type[0][0]
            jobseeker_dict = {
                'firstname': res.get('arbetssokande', {}).get('fornamn', 'MISSING FIRSTNAME'),
                'lastname': res.get('arbetssokande', {}).get('efternamn', 'MISSING LASTNAME'),
                'customer_id': customer_id,
                'social_sec_nr': res.get('arbetssokande', {}).get('personnummer'),
                'customer_since': res.get('processStatus', {}).get('aktuellSedanDatum'),
                'share_info_with_employers': res.get('medgivande', {}).get('infoTillArbetsgivare'),
                'phone': res.get('kontaktuppgifter', {}).get('telefonBostad'),
                'work_phone': res.get('kontaktuppgifter', {}).get('telefonArbetet'),
                'mobile': res.get('kontaktuppgifter', {}).get('telefonMobil'),
                'jobseeker_category_id': skat and skat.id,
                'deactualization_date': res.get('processStatus', {}).get('avaktualiseringsDatum'),
                'deactualization_reason': res.get('processStatus', {}).get('avaktualiseringsOrsaksKod'),
                'email': res.get('kontaktuppgifter', {}).get('epost'),
                'office_id': office and office.id,
                'state_id': state and state.id,
                'registered_through': registered_through,
                'user_id': user and user.id,
                'sms_reminders': res.get('medgivande', {}).get('paminnelseViaSms'),
                'next_contact_date': res.get('kontakt', {}).get('nastaKontaktdatum'),
                'next_contact_time': res.get('kontakt', {}).get('nastaKontaktTid'),
                'next_contact_type': next_contact_type,
                'last_contact_date': res.get('kontakt', {}).get('senasteKontaktdatum'),
                'last_contact_type': last_contact_type,
                'is_jobseeker': True,

            }

            if sun and education_level:
                if partner:
                    if partner.education_ids.filtered(
                            lambda e: e.sun_id == sun and
                            e.education_level_id == education_level):
                        # Already exists. Do nothing.
                        pass
                    else:
                        # TODO: Should we really overwrite educations?
                        jobseeker_dict['education_ids'] = [(5,)]
                else:
                    jobseeker_dict['education_ids'] = []
                if 'education_ids' in jobseeker_dict:
                    jobseeker_dict['education_ids'].append((0, 0, {
                        'sun_id': sun.id,
                        'education_level_id': education_level.id}))
            if partner:
                partner.write(jobseeker_dict)
            else:
                partner = self.env['res.partner'].create(jobseeker_dict)

            for address in res.get('kontaktuppgifter', {}).get('adresser', {}):
                streetaddress = address.get('gatuadress')
                if streetaddress:
                    streetadress_array = streetaddress.split(",")
                    if len(streetadress_array) == 1:
                        street = streetadress_array[0]
                        street2 = False
                    elif len(streetadress_array) > 1:
                        street = streetadress_array[1]
                        street2 = streetadress_array[0]
                    zip = address.get('postnummer')
                    city = address.get('postort')
                    country = address.get('landsadress')
                    if country:
                        country = self.env['res.country'].with_context(lang='sv_SE').search([('name', '=', country)])
                        country = country or None
                    if address.get('adressTyp') == 'FBF':
                        partner.street = street
                        partner.street2 = street2
                        partner.zip = zip
                        partner.city = city
                        partner.country_id = country and country.id
                    elif address.get('adressTyp') == 'EGEN' or address.get('adressTyp') == 'UTL':
                        # TODO: This looks sketchy. Wont this create new
                        #  adresses every time we sync?
                        given_address_dict = {
                            'parent_id': partner.id,
                            'street': street,
                            'street2': street2,
                            'zip': zip,
                            'city': city,
                            'type': 'given address',
                            'country_id': country and country.id,
                        }
                        self.env['res.partner'].create(given_address_dict)
        except Exception:
            em = traceback.format_exc()
            log.log_message(process_name, eventid, RASK_SYNC,
                            objectid=customer_id, error_message=em, status=False)
            return

        log.log_message(process_name, eventid, "SYNC COMPLETED", objectid=customer_id)
        return True
