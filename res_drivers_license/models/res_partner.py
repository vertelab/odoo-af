# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2017 Vertel AB (<http://vertel.se>).
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
import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.one
    def _has_drivers_license(self):
        self.har_drivers_license = len(self.drivers_license_ids) > 0

    has_drivers_license = fields.Boolean(string="Has drivers license", compute=_has_drivers_license)
    drivers_license_ids = fields.One2many(comodel_name='res.drivers_license', inverse_name='partner_id',
                                          string='Drivers license class')
    has_car = fields.Boolean(string="Has access to car")


class ResDriversLicense(models.Model):
    _name = 'res.drivers_license'
    _description = "RES Drivers License"

    partner_id = fields.Many2one(comodel_name="res.partner")
    name = fields.Char(string='Class', required=True)  # A,B etc.
    description = fields.Char(string='Description')
