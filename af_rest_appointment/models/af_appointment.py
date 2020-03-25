# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api, _
from datetime import datetime
from urllib import request
from urllib.error import URLError, HTTPError
import json
import logging
from odoo.exceptions import Warning

# TODO: only use this in remote tests
import ssl

_logger = logging.getLogger(__name__)


class AfAppointment(models.Model):
    _name = "af.appointment"

    # resource-planning/competencies/schedules
    def get_schedules(self, from_datetime, to_datetime, competences):
        client_id = self.env['ir.config_parameter'].sudo().get_param('af_rest.client_id')
        client_secret = self.env['ir.config_parameter'].sudo().get_param('af_rest.client_secret')
        af_environment = self.env['ir.config_parameter'].sudo().get_param('af_rest.af_environment')
        af_port = self.env['ir.config_parameter'].sudo().get_param('af_rest.ipf_port')
        af_url = self.env['ir.config_parameter'].sudo().get_param('af_rest.ipf_url')
        af_system_id = self.env['ir.config_parameter'].sudo().get_param('af_rest.af_system_id')
        
        if not (af_url or af_port or client_id or client_secret or af_environment or af_system_id):
            raise Warning('Please setup AF integrations')

        # try:

        # Convert list of competences into a string to be used in url
        comp = ""

        # TODO : change competences argument to competence-class instead of list of ids.
        for competence in competences:
            comp += "&competence_id=" + competence

        # Generate a tracking-id
        tracking_number = datetime.now().strftime("%y%m%d%H%M%S")
        af_tracking_id = af_system_id.upper() + af_environment.upper() + tracking_number

        # Define base url
        # https://ipfapi.arbetsformedlingen.se:443/appointments/v1/resource-planning/competencies/schedules?from_date=2020-03-17T00:00:00Z&client_id=XXXXXXXXX&client_secret=XXXXXXXXX&to_date=2020-03-25T00:00:00Z&competence_id=ded72445-e5d3-4e21-a356-aad200dac83d
        base_url = "{url}:{port}/{path}?client_id={client}&client_secret={secret}&from_date={from_date}&to_date={to_date}{comps}"
        
        # Insert values into base_url
        get_url = base_url.format(
            url = af_url, # https://ipfapi.arbetsformedlingen.se
            port = af_port, # 443
            path = "appointments/v1/resource-planning/competencies/schedules", # TODO: remove hardcoding?
            client = client_id, # check in anypoint for example
            secret = client_secret, # check in anypoint for example
            from_date = from_datetime, # 2020-03-17T00:00:00Z
            # from_date = from_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"), # 2020-03-17T00:00:00Z - add this line to change expected argument to Datetime-object
            to_date = to_datetime, # 2020-03-25T00:00:00Z
            # to_date = to_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"), # 2020-03-25T00:00:00Z - add this line to change expected argument to Datetime-object
            comps = comp, # &competence_id=ded72445-e5d3-4e21-a356-aad200dac83d
        )
        
        # Generate headers for our get
        get_headers = {
            'AF-Environment': af_environment,
            'AF-SystemId': af_system_id,
            'AF-TrackingId': af_tracking_id,
        }

        # Build or request using url and headers
        # Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)
        req = request.Request(url=get_url, headers=get_headers)

        ctx= ''
        #TODO: only use this code in remote tests
        # tell odoo to ignore cert
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        # TODO: remove this code to test with simulated response
        # open and read request
        res_json = request.urlopen(req, context=ctx).read()
        
        # TODO: add this code to test with simulated response
        # simulate (short) response
        # res_json = '[{"schedule_day": "2020-03-17","competence": {"id": "ded72445-e5d3-4e21-a356-aad200dac83d","name": "Första planeringssamtal (BK1)"},"schedules": [{"end_time": "2020-03-17T09:30:00Z","estimated_service_level": 0.50124635478077317,"forecasted_agents": 297.259,"scheduled_agents": 149,"scheduled_heads": 149,"start_time": "2020-03-17T09:00:00Z"},{"end_time": "2020-03-17T10:00:00Z","estimated_service_level": 0.50124635478077317,"forecasted_agents": 297.259,"scheduled_agents": 149,"scheduled_heads": 149,"start_time": "2020-03-17T09:30:00Z"}]},{"schedule_day": "2020-03-18","competence": {"id": "ded72445-e5d3-4e21-a356-aad200dac83d","name": "Första planeringssamtal (BK1)"},"schedules": [{"end_time": "2020-03-18T09:30:00Z","estimated_service_level": 0.36668357497385418,"forecasted_agents": 297.259,"scheduled_agents": 109,"scheduled_heads": 109,"start_time": "2020-03-18T09:00:00Z"}]}]'

        # Convert json to python format: https://docs.python.org/3/library/json.html#json-to-py-table 
        res = json.loads(res_json)
        
        # Create calendar.event from res
        # res: list of dicts with list of schedules
        # schedules: list of dicts of slots
        for comp_day in res:
            competence_name = comp_day.get('competence').get('name')
            for schedule in comp_day.get('schedules'):
                start_time = datetime.strptime(schedule.get('start_time'), "%Y-%m-%dT%H:%M:%SZ")
                stop_time = datetime.strptime(schedule.get('end_time'), "%Y-%m-%dT%H:%M:%SZ")
                # TODO: rewrite to use calendar.slot instead
                # TODO: check if calendar.slot already exists 
                
                # slots can exist every half hour from 09:00 to 16:00
                # slot = self.env['calendar.slot'].search([('competence','=',???), ('start','=',start_time)])
                if slot:
                    # TODO: update slot with new values
                    pass
                else:
                    vals = {
                        'name': competence_name,
                        'start': start_time,
                        'stop': stop_time,
                        # 'scheduled_agents': schedule.get('scheduled_agents'), # number of agents supposed to be available for this
                        # 'forecasted_agents': schedule.get('forecasted_agents'), # May be implemented at a later date.
                        # 'competence': competences,
                        # TODO: add more data...
                    }
                    # Create calendar.event TODO: change to slot
                    self.env['calendar.event'].create(vals)
                    # self.env['calendar.slot'].create(vals)

        
        # except:
        #     _logger.error('Appointment url error.')
