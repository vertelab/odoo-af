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
        if self._context.get("active_model") == 'calendar.appointment':
            return self.env["calendar.appointment"].browse(self._context.get("active_id"))

    @api.model
    def _get_appointment_start(self):
        if self._context.get("active_model") == 'calendar.appointment':
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
    type_id = fields.Many2one(
        string="Meeting type", related="appointment_id.type_id", readonly=True
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
        ] if self._context.get("active_model") == 'calendar.appointment' else [],
    )
    start = fields.Datetime(string="New start", default=_get_appointment_start)

    @api.multi
    def check_access_planner_locations(self, locations):
        """Check if current user is planner with access to these locations."""
        if not self.env.user.has_group('af_security.af_meeting_planner'):
            return False
        if not self.mapped('appointment_id.operation_id.location_id') in locations:
            return False
        return True

    def action_change_user_appointment(self):
        # Perform access control.
        allowed = False
        denied = False
        locations = self.env.user.mapped('employee_ids.office_ids.operation_ids.location_id')
        # Check access for Meeting Planner
        if self.check_access_planner_locations(locations):
            allowed = True
        if allowed and not denied:
            # Checks passed. Run inner function with sudo.
            return self.sudo()._action_change_user_appointment()
        raise Warning(_('You are not allowed to create these occasions.'))

    def _action_change_user_appointment(self):
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

