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
import logging

_logger = logging.getLogger(__name__)

class CalendarSchedule(models.Model):
    _name = 'calendar.appointment'
    _description = "Appointment"

    name = fields.Char(string='Schedule name', required=True)
    start = fields.Datetime(string='Start', required=True, help="Start date of a schedule")
    stop = fields.Datetime(string='Stop', required=True, help="Stop date of a schedule")
    duration = fields.Float('Duration')
    user_id = fields.Many2one(string='Case worker', comodel_name='res.user', help="Booked case worker")
    partner_id = fields.Many2one(string='Case worker', comodel_name='res.partner', help="Booked customer")
    app_type = fields.Char(string='Type')
    status = fields.Char(string='Status')
    location_code = fields.Char(string='Location')
    office_code = fields.Char(string='Office')