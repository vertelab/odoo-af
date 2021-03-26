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

from odoo.exceptions import Warning

from odoo import models, fields, api, _

from .calendar_constants import *

_logger = logging.getLogger(__name__)


class CalendarAppointmentSuggestion(models.Model):
    _name = "calendar.appointment.suggestion"
    _description = "Bookable Occasion"

    appointment_id = fields.Many2one(
        comodel_name="calendar.appointment", ondelete="cascade"
    )
    start = fields.Datetime()
    stop = fields.Datetime()
    duration = fields.Float(string="Duration")
    duration_text = fields.Char(string="Duration", compute="compute_duration_text")
    occasion_ids = fields.Many2many(
        comodel_name="calendar.occasion", string="Occasions"
    )
    type_id = fields.Many2one(string="Type", comodel_name="calendar.appointment.type")
    channel = fields.Many2one(string="Channel", comodel_name="calendar.channel")
    operation_id = fields.Many2one(comodel_name="hr.operation", string="Operation")
    office_id = fields.Many2one(
        comodel_name="hr.department",
        related="operation_id.department_id",
        string="Office",
        readonly=True,
    )
    user_id = fields.Many2one(comodel_name="res.users", string="Case worker")
    weekday = fields.Char(string="Weekday", compute="_compute_weekday")

    @api.one
    def compute_duration_text(self):
        if self.duration == 0.5:
            self.duration_text = "30 minutes"
        elif self.duration == 1.0:
            self.duration_text = "1 hour"

    @api.one
    def _compute_weekday(self):
        if self.start:
            self.weekday = DAYNUM2DAYNAME[self.start.weekday()]

    @api.multi
    def af_check_access(self):
        """Check access for certain operations.
        This covers the following operations:
        * select_suggestion_move
        * select_suggestion
        """
        allowed = False
        denied = False
        locations = self.env.user.mapped(
            "employee_ids.office_ids.operation_ids.location_id"
        )
        for suggestion in self:
            # Check access for Meeting Planner
            if suggestion.appointment_id.check_access_planner_locations(locations):
                allowed = True
            # Check jobseeker access
            elif suggestion.appointment_id.check_access_jobseeker_officer():
                allowed = True
            else:
                # access denied by all checks
                denied = True
        return allowed and not denied

    @api.multi
    def select_suggestion(self):
        # Perform access control.
        if self.af_check_access():
            # Checks passed. Run inner function with sudo.
            return self.sudo()._select_suggestion()
        raise Warning(_("You are not allowed to handle these meetings."))

    @api.multi
    def _select_suggestion(self):
        # check state of appointment
        if self.appointment_id.state in ["reserved", "confirmed"]:
            raise Warning(_("This appointment is already booked."))

        occasions = self.env["calendar.occasion"]
        for occasion in self.occasion_ids:
            # Ensure that occasions are still free
            if not occasion.appointment_id:
                occasions |= occasion
            else:
                free_occasion = occasion.search(
                    [
                        ("start", "=", self.start),
                        ("type_id", "=", self.type_id.id),
                        ("appointment_id", "=", False),
                    ],
                    limit=1,
                )
                if not free_occasion:
                    raise Warning(
                        _(
                            "No free occasions. This shouldn't happen. Please contact the system administrator."
                        )
                    )

                occasions |= free_occasion

        app_vals = {}

        if self.channel == self.env.ref("calendar_channel.channel_local"):
            app_vals["user_id"] = occasions[0].user_id.id

        app_vals["state"] = "confirmed"
        app_vals["start"] = self.start
        app_vals["stop"] = self.stop

        # Write data to appointment_id
        occasions.write({"appointment_id": self.appointment_id.id})
        self.appointment_id.write(app_vals)

    @api.multi
    def select_suggestion_move(self):
        # Perform access control.
        if self.af_check_access():
            # Checks passed. Run inner function with sudo.
            return self.sudo()._select_suggestion_move()
        raise Warning(_("You are not allowed to handle these meetings."))

    @api.multi
    def _select_suggestion_move(self):
        occasions = self.env["calendar.occasion"]
        for occasion in self.occasion_ids:
            # Ensure that occasions are still free
            if not occasion.appointment_id:
                occasions |= occasion
            else:
                free_occasion = occasion.search(
                    [
                        ("start", "=", self.start),
                        ("type_id", "=", self.type_id.id),
                        ("appointment_id", "=", False),
                    ],
                    limit=1,
                )
                if not free_occasion:
                    raise Warning(
                        _(
                            "No free occasions. This shouldn't happen. Please contact the system administrator."
                        )
                    )

                occasions |= free_occasion
        self.appointment_id.move_appointment(
            occasions, self.appointment_id.cancel_reason
        )
