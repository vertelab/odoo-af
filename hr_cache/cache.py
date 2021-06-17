# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2019 Vertel AB (<http://vertel.se>).
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
from odoo.exceptions import except_orm, Warning, RedirectWarning
from odoo.http import request

import odoo
from odoo import SUPERUSER_ID
from odoo import http
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class cache(models.TransientModel):
    _name = 'hr.cache'
    _description = "HR Cache"
    _transient_max_hours = 120

    employee_id = fields.Integer()
    barcode = fields.Char()

    # @api.model
    # def create_cache(self):
    #     cache = self.env['hr.cache'].search('employee_id', '=', employee_id)
    #     if cache:
    #         cache.employee_id = employee_id
    #         cache.barcode = barcode
    #     else:
    #         self.env['hr.cache'].create({
    #             'barcode':employee_id.barcode
    #             'employee_id':employee_id
    #             })
