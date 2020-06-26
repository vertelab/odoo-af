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

import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta

import pytz
import copy

_logger = logging.getLogger(__name__)


class BookMeeting(models.TransientModel):
    _name = 'calendar.book_meeting'
    _description = 'Book Meeting'

    user_id = fields.Many2many(string='Case worker', comodel_name='res.users', help="Booked case worker")
    partner_id = fields.Many2many(string='Customer', comodel_name='res.partner', help="Booked customer")
    desired_date = fields.DateTime(string='Desired date', required=True, help="Choose a desired date for an appointment")
    duration = fields.Float('Duration')
    type_id = fields.Many2one(string='Type', comodel_name='calendar.appointment.type')
    office = fields.Many2one('res.partner', string="Office")
    description = fields.Text(string='Description')
    

    def action_book_meeting(self):
        numbers = [number.strip() for number in self.recipients.split(',') if number.strip()]

        active_model = self.env.context.get('active_model')
        if active_model and hasattr(self.env[active_model], 'message_post_send_sms'):
            model = self.env[active_model]
            records = self._get_records(model)
            records.message_post_send_sms(self.message, numbers=numbers)
        else:
            self.env['sms.api']._send_sms(numbers, self.message)
        return True
