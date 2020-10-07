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
import requests
from requests.auth import HTTPBasicAuth
import json
from uuid import uuid4
import logging
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)

class Partner(models.Model):
    _inherit = 'res.partner'
    
    ais_a_ids = fields.One2many(comodel_name='res.partner.ais_a', 
                                 string='Cases', 
                                 inverse_name="partner_id", 
                                 compute='compute_ais_a_ids')
    
    @api.multi
    def compute_ais_a_ids(self):
        user = self._context.get('uid')
        user = user and self.env['res.users'].browse(user) or self.env.user
        client_id, client_secret, auth_user, auth_password = self._get_ipf_credentials()
        if not all((user.af_signature, client_id, client_secret, auth_user, auth_password)):
            return
        param = self.env['ir.config_parameter'].sudo()
        ssl_params = {
        }
        verify = param.get_param('ipf_ais_a.ssl_verify', None)
        ssl_cert = param.get_param('ipf_ais_a.ssl_cert', None)
        ssl_key = param.get_param('ipf_ais_a.ssl_key', None)
        if verify == '0':
            ssl_params['verify'] = False
        elif verify:
            ssl_params['verify'] = verify
        if ssl_cert and ssl_key:
            ssl_params['cert'] = (ssl_cert, ssl_key)
        for record in self:
            if record.is_jobseeker:
                url="https://ipfapi.arbetsformedlingen.se:443/ais-beslut-om-stod-read/v1/arenden/sokande/{personnummer}?client_id={client_id}&client_secret={client_secret}"
                personnummer = record.get_ais_a_pnr()
                if personnummer:
                    headers = record._get_ipf_headers()
                    url = url.format(
                        personnummer=personnummer,
                        client_id=client_id,
                        client_secret=client_secret)
                    response = requests.get(
                        url,
                        headers=headers,
                        auth=HTTPBasicAuth(auth_user, auth_password),
                        **ssl_params
                    )
                    res = response.json()
                    record.ais_a_ids = record.env['res.partner.ais_a']
                    for arende in res.get('arenden', []):
                        record.ais_a_ids |= record.env['res.partner.ais_a'].create_arende(arende, record.id)

    @api.multi
    def get_ais_a_pnr(self):
        try:
            if self.company_registry:
                pnr = self.company_registry.replace('-', '')
                return pnr
        except:
            _logger.warn("Invalid personal identification number: %s" % self.company_registry)

    @api.model
    def _get_ipf_credentials(self):
        param = self.env['ir.config_parameter'].sudo()
        return (
            param.get_param('ipf_client_id', None),
            param.get_param('ipf_client_secret', None),
            param.get_param('ipf_ais_a.auth_user', None),
            param.get_param('ipf_ais_a.auth_password', None),
        )

    @api.model
    def _get_ipf_headers(self):
        user = self._context.get('uid')
        user = user and self.env['res.users'].browse(user) or self.env.user
        param = self.env['ir.config_parameter'].sudo()
        return {
            'AF-SystemId': 'AFCRM',
            'AF-Environment': param.get_param('ipf_ais_a.ipf_environment', 'T2'),
       
            'AF-TrackingId': '%s' % uuid4(),
            'AF-EndUserId': user.af_signature,
        }

class PartnerAisA(models.TransientModel):
    _name ='res.partner.ais_a'
    _description = 'AIS-Å Beslut Om Stod'

    name = fields.Integer(string="Case nr")
    res_officer = fields.Char(string='Handlaggare')
    res_office = fields.Char(string='Kontor')
    dec_office = fields.Char(string='Beslutande Kontor')
    status = fields.Char(string='Status')
    status_change = fields.Char(string='Senaste Status Ändring')
    atgard = fields.Char(string='Åtgärd')

    partner_id = fields.Many2one(comodel_name="res.partner", string="Job seeker")

    @api.model
    def create_arende(self, vals, partner_id):
        return self.create({
            'partner_id': partner_id,
            'name': vals['arendenummer'],
            'res_officer' : vals.get('ansvarigHandlaggare', {}).get('signatur'),
            'res_office' : vals.get('ansvarigtKontor', {}).get('namn'),
            'dec_office' : vals.get('beslutandeKontor', {}).get('namn'),
            'status' : vals.get('status', {}).get('benamning'),           
            'status_change' : vals['senasteStatusAndring'],
            'atgard' : vals.get('atgard', {}).get('benamning'),



        })


