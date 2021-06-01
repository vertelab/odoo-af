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
from datetime import datetime
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = 'res.partner'

    case_ids = fields.One2many(comodel_name='res.partner.case',
                               string='Cases',
                               inverse_name="partner_id",
                               compute='compute_case_ids')

    @api.multi
    def compute_case_ids(self):
        for record in self:
            if record.is_jobseeker:
                personnummer = record.get_case_pnr()
                if personnummer:
                    try:
                        ipf = self.env.ref('ipf_case.ipf_endpoint_case').sudo()
                        res = ipf.call(personnummer=personnummer)
                        record.case_ids = record.env['res.partner.case']
                        for arende in res.get('arenden', []):
                            record.case_ids |= record.env['res.partner.case'].create_arende(arende, record.id)
                    except Exception as e:
                        _logger.warning('Error in IPF CASE integration.', exc_info=e)
                        record.case_ids = None

    @api.multi
    def get_case_pnr(self):
        try:
            if self.social_sec_nr:
                pnr = self.social_sec_nr.replace('-', '')
                return pnr
        except ValueError:
            raise UserError("Invalid personal identification number: %s" % self.social_sec_nr)


class PartnerArende(models.TransientModel):
    _name = 'res.partner.case'
    _description = 'Ärende För System'

    source = fields.Char(string='Source')
    name = fields.Char(string="Case number")
    res_officer = fields.Char(string='Case officer')
    status = fields.Char(string='Status')
    start = fields.Date(string='Start date')
    stop = fields.Date(string='End date')
    short_names = fields.Char(string='Short name')
    name_desc = fields.Char(string='Description')
    case_type = fields.Char(string="Case type")
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Job seeker")

    @api.model
    def create_arende(self, vals, partner_id):
        start_date = vals.get('beslut_period', {}).get('startdatum')
        stop_date = vals.get('beslut_period', {}).get('slutdatum')
        short_name = vals['arendetyp_kortnamn']
        name_desc = vals['arendetyp_benamning']

        return self.create({
            'partner_id': partner_id,
            #  AIS is to be changed in future to show BÄR.
            'source': 'AIS',
            'name': vals['arende_id'],
            'res_officer': vals.get('beslut_handlaggare', {}).get('signatur'),
            'status': vals['status'],
            'case_type': f'{name_desc}({short_name})',
            'start': datetime.strptime(start_date, '%Y-%m-%d') if start_date else False,
            'stop': datetime.strptime(stop_date, '%Y-%m-%d') if stop_date else False,
        })
