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

from collections import OrderedDict

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    jobseeker_access = fields.Selection(
        selection=[('STARK', 'Stark'), ('MYCKET_STARK', 'Mycket stark')],
        string='Access Level',
        compute='_compute_jobseeker_access',
        search='_search_jobseeker_access')

    @api.multi
    def _compute_jobseeker_access(self):
        """ Placeholder. The real function is implemented in af_security_rules."""
        pass

    @api.model
    def _search_jobseeker_access(self, op, value):
        """ Placeholder. The real function is implemented in af_security_rules."""
        # Return something that's always True.
        return [('id', '!=', 0)]

    @api.multi
    def _grant_jobseeker_access(
            self,
            access_type,
            user=None,
            reason_code=None,
            reason=None,
            granting_user=None,
            start=None,
            interval=1):
        """ Placeholder. The real function is implemented in af_security_rules."""
        return OrderedDict()


class User(models.Model):
    _inherit = 'res.users'

    af_signature = fields.Char(
        string='AF signature',
        compute='_compute_af_signature',
        store=True)

    @api.depends('login')
    def _compute_af_signature(self):
        for record in self:
            record.af_signature = record.login
