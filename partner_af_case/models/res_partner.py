# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2019 Vertel AB (<http://vertel.se>).
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
import logging
_logger = logging.getLogger(__name__)

class ResPartnerCase(models.Model):
    _description = 'Case for a partner'
    _name = 'res.partner.case'

    name = fields.Char(string="Title") 
    partner_id = fields.Many2one(comodel_name="res.partner", string="Job seeker")

    administrative_officer = fields.Many2one('res.users', string='Administrative officer', default=lambda self: self.env.user)
    case_description = fields.Text(string="Case description")
    # case_date = fields.Datetime(string="Refers to date") 
    # case_type = fields.Many2one(comodel_name="res.partner.case.type") 
    # case_number = fields.Char(string="AIS number")

    # office = fields.Many2one('res.partner', string="Office")
    # customer_id = fields.Char(string="Customer number", related="partner_id.customer_id") 

class ResPartner(models.Model):
    _inherit = 'res.partner'

    case_ids = fields.One2many(comodel_name='res.partner.case', 
                                 string='case', inverse_name="partner_id")

    @api.one
    def compute_case_count(self):
        for partner in self:
            partner.case_count = len(partner.case_ids)

    case_count = fields.Integer(compute='compute_case_count')

    @api.multi
    def view_case(self):
        action = {
            'name': _('Case'),
            'domain': [('partner_id', '=', self.ids)],
            'view_type': 'form',
            'res_model': 'res.partner.case',
            'view_id': self.env.ref('partner_af_case.view_partner_case_tree_button').id, 
            'view_mode': 'tree', 
            'type': 'ir.actions.act_window',
        }
        if len(self) == 1:
            action['context'] = {'default_partner_id': self.id}
        return action

# class ResPartnerCaseType(models.Model):
#     _name="res.partner.case.type"

#     case_id = fields.One2many(comodel_name="res.partner.case", inverse_name="case_type")

#     name = fields.Char(string="Name")
#     description = fields.Char(string="Description")
