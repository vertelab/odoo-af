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

import copy
import logging
import pytz
from datetime import datetime, timedelta
from odoo.exceptions import UserError

from odoo import api, fields, models, _
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)


class CreateLocalOccasion(models.TransientModel):
    _name = "calendar.create_local_occasion"
    _description = "Create occasion"

    # @api.model
    # def _get_appointments(self):
    #     return self.env['calendar.appointment'].browse(self._context.get('active_ids'))

    name = fields.Char(string="Name", required=True)
    start = fields.Datetime(
        string="Start",
        required=True,
        help="Start date of an occasion",
        default=lambda self: datetime.now().replace(minute=0, second=0, microsecond=0),
    )
    stop = fields.Datetime(
        string="Stop", required=True, help="Stop date of an occasion"
    )
    duration_selection = fields.Selection(
        string="Duration",
        selection=[("30 minutes", "30 minutes"), ("1 hour", "1 hour")],
    )
    duration = fields.Float("Duration", required=True)
    type_id = fields.Many2one(
        comodel_name="calendar.appointment.type",
        string="Type",
        required=True,
        domain="[('channel', '=', 'Local')]"
    )
    channel = fields.Many2one(
        string="Channel", comodel_name="calendar.channel", related="type_id.channel", readonly=True
    )
    channel_name = fields.Char(string="Channel", related="channel.name")
    user_ids = fields.Many2many(
        string="Case worker",
        comodel_name="res.users",
        help="Booked case worker",
        required=True,
    )
    operation_id = fields.Many2one(comodel_name="hr.operation", string="Operation")
    location_ids = fields.Many2many(comodel_name='hr.location', string="Allowed Locations", default=lambda self: self.default_location_ids())
    # fields describing how to create occasions:
    create_type = fields.Selection(
        string="Type",
        selection=[
            ("single", "Single"),
            ("repeating", "Repeating"),
        ],
        default="single",
        required=True,
    )
    start_range = fields.Date(string="Start of repeat")
    stop_range = fields.Date(string="End of repeat")
    repeat_mon = fields.Boolean(string="Monday")
    repeat_tue = fields.Boolean(string="Tuesday")
    repeat_wed = fields.Boolean(string="Wednesday")
    repeat_thu = fields.Boolean(string="Thursday")
    repeat_fri = fields.Boolean(string="Friday")

    @api.model
    def default_location_ids(self):
        return self.env.user.mapped('employee_ids.office_ids.operation_ids.location_id')

    @api.onchange("type_id")
    def set_duration_selection(self):
        self.name = (self.type_id.name,)
        self.duration = self.type_id.duration / 60.0

        if self.duration == 0.5:
            self.duration_selection = "30 minutes"
        elif self.duration == 1.0:
            self.duration_selection = "1 hour"

    @api.onchange("duration_selection")
    def set_duration(self):
        if self.duration_selection == "30 minutes":
            self.duration = 0.5
        if self.duration_selection == "1 hour":
            self.duration = 1.0
        self.onchange_duration_start()

    @api.onchange("duration", "start")
    def onchange_duration_start(self):
        if self.start and self.duration:
            self.stop = self.start + timedelta(minutes=int(self.duration * 60))

    @api.multi
    def check_access_planner_locations(self, locations):
        """Check if current user is planner with access to these locations."""
        if not self.env.user.has_group('af_security.af_meeting_planner'):
            return False
        if not self.mapped('operation_id.location_id') in locations:
            return False
        return True

    def action_create_occasions(self):
        """Create occasions."""
        # Perform access control.
        allowed = False
        denied = False
        locations = self.env.user.mapped('employee_ids.office_ids.operation_ids.location_id')
        # Check access for Meeting Planner
        if self.check_access_planner_locations(locations):
            allowed = True
        if allowed and not denied:
            # Checks passed. Run inner function with sudo.
            return self.sudo()._action_create_occasions()
        raise Warning(_('You are not allowed to create these occasions.'))

    def _action_create_occasions(self):
        if not (
            (self.start.minute in [0, 30] and self.stop.second == 0)
            and (self.stop.minute in [0, 30] and self.stop.second == 0)
        ):
            raise Warning("Start or stop time is not and exacly an hour or halfhour.")

        # Check how many 30min occasions we need
        no_occ = int(self.duration / 0.5)
        if self.create_type == "single":
            # check if date is a holiday
            # TODO: do we do this check in check_resource_calendar_occasion() now?
            if not self.env["calendar.appointment"]._check_resource_calendar_date(
                self.start
            ):
                raise Warning("This day is a holiday.")

            for user_id in self.user_ids:
                for curr_occ in range(no_occ):
                    curr_start = self.start + timedelta(minutes=curr_occ * 30)
                    if user_id.check_resource_calendar_occasion(curr_start):
                        occ = self.env["calendar.occasion"]._force_create_occasion(
                            30,
                            curr_start,
                            self.type_id.id,
                            self.channel.id,
                            "request",
                            user_id,
                            self.operation_id,
                            False,
                        )
            res = self.env.ref("calendar_af.action_calendar_local_occasion").read()[0]
            res["domain"] = [
                ("user_id", "in", self.user_ids._ids),
            ]
            return res
        elif self.create_type == "repeating":
            # create list of weekday values allowed:
            repeat_list = []
            if self.repeat_mon:
                repeat_list.append(0)
            if self.repeat_tue:
                repeat_list.append(1)
            if self.repeat_wed:
                repeat_list.append(2)
            if self.repeat_thu:
                repeat_list.append(3)
            if self.repeat_fri:
                repeat_list.append(4)
            # create a list of all days in start-end-range.
            date_list = [
                self.start + timedelta(days=x)
                for x in range((self.stop_range - self.start_range).days)
            ]
            # loop possible dates
            for date in date_list:
                # update date, keep start time.
                start_date = self.start.replace(
                    year=date.year, month=date.month, day=date.day
                )
                # check if date is an allowed weekday
                # TODO: do we do this check in check_resource_calendar_occasion() now?
                if start_date.weekday() in repeat_list and self.env[
                    "calendar.appointment"
                ]._check_resource_calendar_date(start_date):
                    # create only 30 min occasions (if duration is longer, create several occasions):
                    for user_id in self.user_ids:
                        for curr_occ in range(no_occ):
                            curr_start = start_date + timedelta(minutes=curr_occ * 30)
                            if user_id.check_resource_calendar_occasion(curr_start):
                                occ = self.env["calendar.occasion"]._force_create_occasion(
                                    30,
                                    curr_start,
                                    self.type_id.id,
                                    self.channel.id,
                                    "request",
                                    user_id,
                                    self.operation_id,
                                    False,
                                )
            res = self.env.ref("calendar_af.action_calendar_local_occasion").read()[0]
            res["domain"] = [
                ("user_id", "in", self.user_ids._ids),
            ]
            return res
        return False
