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

from datetime import timedelta

import logging

from odoo import api, fields, models, _


_logger = logging.getLogger(__name__)


class ChangeUserAppointment(models.TransientModel):
    _name = "calendar.change_user_appointment"
    _description = "Change case worker"

    @api.model
    def _get_appointment(self):
        return self.env["calendar.appointment"].browse(self._context.get("active_id"))

    @api.model
    def _get_appointment_start(self):
        return (
            self.env["calendar.appointment"]
            .browse(self._context.get("active_id"))
            .start
        )

    appointment_id = fields.Many2one(
        string="Appointment",
        comodel_name="calendar.appointment",
        default=_get_appointment,
    )
    duration = fields.Float(
        string="Duration", related="appointment_id.duration", readonly=True
    )
    now_user_id = fields.Many2one(
        string="Case worker",
        comodel_name="res.users",
        related="appointment_id.user_id",
        readonly=True,
    )
    new_user_id = fields.Many2one(
        string="New case worker",
        comodel_name="hr.employee",
        domain=lambda self: [
            (
                "id",
                "in",
                self.env["calendar.appointment"]
                .browse(self._context.get("active_id"))
                .office_id.employee_ids._ids,
            )
        ],
    )
    start = fields.Datetime(string="New start", default=_get_appointment_start)

    def action_change_user_appointment(self):
        # TODO: add check that case worker is indeed free
        if self.appointment_id.start != self.start:
            self.appointment_id.start = self.start
            self.appointment_id.stop = self.start + timedelta(
                minutes=60 * self.duration
            )
        self.appointment_id.user_id = self.new_user_id.user_id
        self.appointment_id.additional_booking = False
        if self.appointment_id.occasion_ids:
            for i, occasion in enumerate(self.appointment_id.occasion_ids):
                if self.appointment_id.start != self.start:
                    occasion.start = self.start + timedelta(minutes=30 * i)
                    occasion.stop = self.start + timedelta(minutes=30 + 30 * i)
                occasion.user_id = self.new_user_id.user_id
                occasion.additional_booking = False
        return True