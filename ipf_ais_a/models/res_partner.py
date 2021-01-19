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

import json
import logging
import requests
from odoo.exceptions import Warning
from requests.auth import HTTPBasicAuth
from uuid import uuid4

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = 'res.partner'

    ais_a_ids = fields.One2many(comodel_name='res.partner.ais_a',
                                string='Cases',
                                inverse_name="partner_id",
                                compute='compute_ais_a_ids')

    @api.multi
    def compute_ais_a_ids(self):
        for record in self:
            if record.is_jobseeker:
                personnummer = record.get_ais_a_pnr()
                if personnummer:
                    try:
                        ipf = self.env.ref('af_ipf.ipf_endpoint_ais_a').sudo()
                        res = ipf.call(personnummer=self.social_sec_nr)
                        record.ais_a_ids = record.env['res.partner.ais_a']
                        for arende in res.get('arenden', []):
                            record.ais_a_ids |= record.env['res.partner.ais_a'].create_arende(arende, record.id)
                    except Exception as e:
                        _logger.warn('Error in IPF AIS-Å integration.', exc_info=e)
                        record.ais_a_ids = None

    @api.multi
    def get_ais_a_pnr(self):
        try:
            if self.social_sec_nr:
                pnr = self.social_sec_nr.replace('-', '')
                return pnr
        except:
            _logger.warn("Invalid personal identification number: %s" % self.social_sec_nr)


class PartnerAisA(models.TransientModel):
    _name = 'res.partner.ais_a'
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
            'res_officer': vals.get('ansvarigHandlaggare', {}).get('signatur'),
            'res_office': vals.get('ansvarigtKontor', {}).get('namn'),
            'dec_office': vals.get('beslutandeKontor', {}).get('namn'),
            'status': vals.get('status', {}).get('benamning'),
            'status_change': vals['senasteStatusAndring'],
            'atgard': vals.get('atgard', {}).get('benamning'),

        })
