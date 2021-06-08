# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2021 Vertel AB (<http://vertel.se>).
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
from odoo.exceptions import ValidationError

from .calendar_constants import *

_logger = logging.getLogger(__name__)


class CalendarAppointmentType(models.Model):
    _name = "calendar.appointment.type"
    _description = "Meeting type"
    _order = "sort_order"

    sort_order = fields.Integer(string="Sort order", required=True)
    name = fields.Char("Meeting type name", required=True)
    ipf_id = fields.Char(
        "Teleopti competence id",
        required=True,
        help="The IPF type id, if this is wrong the integration won't work",
    )
    ipf_name = fields.Char("Teleopti competence name")
    channel = fields.Many2one(string="Channel", comodel_name="calendar.channel")
    duration = fields.Float(string="Duration", compute="_comp_duration", store=True)
    duration_30 = fields.Boolean(string="30 min")
    duration_60 = fields.Boolean(string="60 min")
    days_first = fields.Integer(string="First allowed day for type")
    days_last = fields.Integer(string="Last allowed day for type")
    ipf_num = fields.Integer(string="Meeting type id")
    additional_booking = fields.Boolean(string="Over booking")
    text = fields.Text(string="Comment")

    @api.depends("duration_30", "duration_60")
    def _comp_duration(self):
        for channel in self:
            if channel.duration_30:
                channel.duration = 30.0
            elif channel.duration_60:
                channel.duration = 60.0
            else:
                channel.duration = False

    @api.one
    @api.constrains("duration_30", "duration_60")
    def _check_duration_30_60(self):
        if self.duration_30 and self.duration_60:
            raise ValidationError(
                _(
                    "Meeting type \"{type_name}\" can't have two different durations."
                ).format(type_name=self.name)
            )
        if not (self.duration_30 or self.duration_60):
            raise ValidationError(
                _(
                    "Meeting type \"{type_name}\" needs a duration."
                ).format(type_name=self.name)
            )

class CalendarChannel(models.Model):
    _name = "calendar.channel"
    _description = "Channel"

    name = fields.Char("Name", translate=True, required=True)


class CalendarMappedDates(models.Model):
    _name = "calendar.mapped_dates"
    _description = "Mapped dates"

    name = fields.Char(string="Name")
    from_date = fields.Date(string="From Date", required=True)
    to_date = fields.Date(string="To Date", required=True)
    operation_id = fields.Many2one(comodel_name="hr.operation", string="Operation")


class CalendarAppointmentCancelReason(models.Model):
    _name = "calendar.appointment.cancel_reason"
    _description = "Cancellation reason for an appointment"

    name = fields.Char(string="Name", required=True, translate=True)
    appointment_id = fields.One2many(
        comodel_name="calendar.appointment", inverse_name="cancel_reason"
    )
