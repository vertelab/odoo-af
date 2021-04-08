# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2020 Vertel AB (<http://vertel.se>).
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


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    office_id = fields.Many2one('hr.department', string='Office')
    office_ids = fields.Many2many(
        'hr.department',
        relation='hr_department_office_partner_rel',
        column1='partner_id',
        column2='office_id',
        string='Offices')

    @api.one
    # @api.onchange('office_id')
    def update_office_ids(self):
        """Add office_id to office_ids."""
        if self.office_id not in self.office_ids:
            self.office_ids |= self.office_id

    @api.multi
    def write(self, vals):
        res = super(HrEmployee, self).write(vals)
        if 'office_id' in vals:
            self.update_office_ids()
        return vals

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        records = super(HrEmployee, self).create(vals_list)
        records.update_office_ids()
        return records
