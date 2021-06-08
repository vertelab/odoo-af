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
from datetime import timedelta
from odoo.exceptions import ValidationError

from odoo import models, fields, api, _

from .calendar_constants import *

_logger = logging.getLogger(__name__)


class CalendarAppointment(models.Model):
    _name = "calendar.appointment"
    _description = "Appointment"

    @api.model
    def _local_user_domain(self):
        if self.partner_id:
            res = []
            # res.append(('partner_id.operation_id.id', '=', self.env.user.operation_id.id))

            # TODO: add hr.skill check ('type_id.skills_ids', 'in', self.env.user.skill_ids)
            # TODO: add check if case worker has occasions and that these are free. Maybe use a computed field on res.users?
        else:
            res = []
        return res

    name = fields.Char(string="Name", required=True)
    start = fields.Datetime(
        string="Start",
        required=True,
        help="Start date of an appointment",
        default=lambda self: datetime.now(),
    )
    stop = fields.Datetime(
        string="Stop", required=True, help="Stop date of an appointment"
    )
    duration_selection = fields.Selection(
        string="Duration",
        selection=[("30 minutes", "30 minutes"), ("1 hour", "1 hour")],
    )
    duration_text = fields.Char(
        string="Duration", compute="compute_duration_text", store=True
    )
    duration = fields.Float("Duration")
    user_id = fields.Many2one(
        string="Case worker", comodel_name="res.users", help="Booked case worker"
    )
    user_id_local = fields.Many2one(
        string="Case worker",
        comodel_name="res.users",
        help="Booked case worker",
        domain=_local_user_domain,
    )
    partner_id = fields.Many2one(
        string="Customer",
        comodel_name="res.partner",
        help="Booked customer",
        default=lambda self: self.default_partners(),
    )
    state = fields.Selection(
        selection=[
            ("free", "Draft"),
            ("reserved", "Reserved"),
            ("confirmed", "Confirmed"),
            ("done", "Done"),
            ("canceled", "Canceled"),
        ],
        string="State",
        default="free",
        help="Status of the meeting",
    )
    cancel_reason = fields.Many2one(
        string="Cancel reason",
        comodel_name="calendar.appointment.cancel_reason",
        help="Cancellation reason",
    )
    cancel_reason_temp = fields.Many2one(
        string="Cancel reason",
        comodel_name="calendar.appointment.cancel_reason",
        store=False,
        help="Cancellation reason",
    )
    operation_id = fields.Many2one(string="Operation", comodel_name="hr.operation")
    office_id = fields.Many2one(
        comodel_name="hr.department",
        string="Office",
        related="operation_id.department_id",
        readonly=True,
    )
    occasion_ids = fields.One2many(
        comodel_name="calendar.occasion",
        inverse_name="appointment_id",
        string="Occasion",
    )
    type_id = fields.Many2one(
        string="Type", required=True, comodel_name="calendar.appointment.type"
    )
    channel = fields.Many2one(
        string="Channel",
        required=True,
        comodel_name="calendar.channel",
        related="type_id.channel",
        readonly=True,
    )
    channel_name = fields.Char(
        string="Channel", related="type_id.channel.name", readonly=True
    )
    additional_booking = fields.Boolean(
        String="Over booking", related="occasion_ids.additional_booking"
    )
    reserved = fields.Datetime(
        string="Reserved", help="Occasions was reserved at this date and time"
    )
    description = fields.Text(string="Description")
    suggestion_ids = fields.One2many(
        comodel_name="calendar.appointment.suggestion",
        inverse_name="appointment_id",
        string="Suggested Dates",
    )
    case_worker_name = fields.Char(
        string="Case worker", compute="_compute_case_worker_name"
    )
    active = fields.Boolean(string="Active", default=True)
    show_suggestion_ids = fields.Boolean(string="Show suggestions", default=False)
    weekday = fields.Selection(
        string="Weekday",
        selection=[
            (0, "Monday"),
            (1, "Tuesday"),
            (2, "Wednesday"),
            (3, "Thursday"),
            (4, "Friday"),
            (5, "Saturday"),
            (6, "Sunday"),
        ],
        compute="_compute_weekday",
    )
    start_time = fields.Char(
        string="Appointment start time",
        readonly=True,
        compute="_app_start_time_calc",
        store=True,
    )

    @api.one
    @api.depends("duration")
    def compute_duration_text(self):
        if self.duration == 0.5:
            self.duration_text = _("30 minutes")
        elif self.duration == 1.0:
            self.duration_text = _("1 hour")
        else:
            self.duration_text = self.duration

    @api.depends("start")
    def _app_start_time_calc(self):
        offset = int(
            self[0]
            .start.astimezone(pytz.timezone(LOCAL_TZ))
            .utcoffset()
            .total_seconds()
            / 60
            / 60
        )
        for app in self:
            app.start_time = "%s:%s" % (
                str(app.start.hour + offset).rjust(2, "0"),
                str(app.start.minute).ljust(2, "0"),
            )

    @api.one
    def _compute_weekday(self):
        if self.start:
            self.weekday = self.start.weekday()

    @api.one
    def _compute_case_worker_name(self):
        if self.channel == self.env.ref("calendar_channel.channel_pdm"):
            self.case_worker_name = _("Employment service officer")
        else:
            self.case_worker_name = f"{self.user_id.login} ({self.user_id.name})"

    @api.model
    def default_partners(self):
        """ When active_model is res.partner, the current partners should be attendees """
        partners = self.env["res.partner"]
        active_id = self._context.get("active_id")
        if self._context.get("active_model") == "res.partner" and active_id:
            if active_id not in partners.ids:
                partners |= self.env["res.partner"].browse(active_id)
        return partners

    @api.onchange("type_id", "partner_id")
    def check_partner_match_area(self):
        if (
            self.type_id
            and not self.partner_id.match_area
            and "KROM" in self.type_id.name
        ):
            self.type_id = False
            raise ValidationError(_("Jobseeker not KROM classified"))

    @api.onchange("type_id")
    def set_duration_selection(self):
        self.name = self.type_id.name
        if self.duration == 0.5:
            self.duration_selection = "30 minutes"
        elif self.duration == 1.0:
            self.duration_selection = "1 hour"

    # Accurate Duration based on Selected Type
    @api.onchange("type_id")
    def set_duration_type(self):
        if self.type_id:
            if self.type_id.duration_30 is True:
                self.duration_selection = "30 minutes"
            elif self.type_id.duration_60:
                self.duration_selection = "1 hour"
            else:
                self.duration_selection = False
        else:
            self.duration_selection = False

    @api.onchange("duration_selection")
    def set_duration(self):
        if self.duration_selection == "30 minutes":
            self.duration = 0.5
        if self.duration_selection == "1 hour":
            self.duration = 1.0

    @api.onchange("partner_id", "user_id", "start", "duration", "type_id", "channel")
    def hide_suggestion_ids(self):
        self.show_suggestion_ids = False

    @api.multi
    def af_check_access(self):
        """Check access for certain operations that require sudo.
        This covers the following operations:
        * compute_suggestion_ids
        """
        allowed = False
        denied = False
        locations = self.env.user.mapped(
            "employee_ids.office_ids.operation_ids.location_id"
        )
        # Check access for Meeting Planner
        if self.check_access_planner_locations(locations):
            allowed = True
        if self.check_access_jobseeker_officer():
            allowed = True
        if allowed and not denied:
            return True
        return False

    @api.multi
    def check_access_planner_locations(self, locations):
        """Check if current user is planner with access to these locations."""
        if not self.env.user.has_group("af_security.af_meeting_planner"):
            return False
        local_channel = self.env.ref("calendar_channel.channel_local")
        for appointment in self:
            # ensure that appointment is local
            if appointment.channel != local_channel:
                return False
            # ensure that user has access to the appointment location.
            if appointment.mapped("operation_id.location_id") not in locations:
                return False
        return True

    @api.multi
    def check_access_jobseeker_officer(self):
        """Check if the user has access to this jobseeker."""
        try:
            # Ensure jobseeker access
            for appointment in self:
                if appointment.partner_id.jobseeker_access not in (
                    "STARK",
                    "MYCKET_STARK",
                ):
                    return False
            return True
        except:
            # Assume Access Error
            return False

    @api.one
    def compute_suggestion_ids(self):
        # Perform access control.
        if self.af_check_access():
            # Checks passed. Run inner function with sudo.
            return self.sudo()._compute_suggestion_ids()
        raise ValidationError(_("You are not allowed to handle these meetings."))

    @api.one
    def _compute_suggestion_ids(self):
        if not all((self.duration, self.type_id, self.channel)):
            return
        if (
            self.channel != self.env.ref("calendar_channel.channel_pdm")
            and not self.operation_id
        ):
            return
        # checking if we allow meetings of this length
        allowed_durations = []
        if self.type_id.duration_60:
            allowed_durations += [1]
        if self.type_id.duration_30:
            allowed_durations += [0.5]
        if self.duration not in allowed_durations:
            raise ValidationError(
                _("This duration is not allowed for the meeting type.")
            )

        start = self.start_meeting_search(self.type_id)
        stop = self.stop_meeting_search(start, self.type_id)
        self.show_suggestion_ids = True
        suggestion_ids = []
        if self.suggestion_ids:
            suggestion_ids.append((5,))
        occasions = self.env["calendar.occasion"].get_bookable_occasions(
            start,
            stop,
            self.duration * 60,
            self.type_id,
            self.operation_id,
            max_depth=1,
        )
        for day in occasions:
            for day_occasions in day:
                for occasion in day_occasions:
                    suggestion_ids.append(
                        (
                            0,
                            0,
                            {
                                # Add occasions-data on suggestions
                                "start": occasion[0].start,
                                "stop": occasion[-1].stop,
                                "duration": len(occasion) * 0.5
                                if len(occasion) != 1
                                else occasion[0].duration,
                                "type_id": occasion[0].type_id.id,
                                "channel": occasion[0].channel.id,
                                "operation_id": occasion[0].operation_id.id,
                                "user_id": occasion[0].user_id,
                                "occasion_ids": [(6, 0, occasion._ids)],
                            },
                        )
                    )
        self.suggestion_ids = suggestion_ids

    @api.onchange("duration", "start")
    def onchange_duration_start(self):
        if self.start and self.duration:
            self.stop = self.start + timedelta(minutes=int(self.duration * 60))

    @api.onchange("channel")
    def onchange_channel(self):
        if self.type_id and (self.channel != self.type_id.channel):
            self.type_id = False
            self.operation_id = False

    @api.onchange("channel_name")
    def onchange_channel_name(self):
        channel = self.env["calendar.channel"].search([("name", "=", self.name)])
        if channel:
            self.channel = channel.id

    @api.onchange("user_id_local")
    def onchange_user_id_local(self):
        if self.user_id_local:
            # TODO: add check and transfer occasions
            free_occ = self.env["calendar.occasion"].search(
                [("id", "in", self.user_id.free_occ), ("start", "=", self.start)]
            )
            if free_occ:
                self.occasion_ids = [(6, 0, free_occ._ids)]
                self.user_id = self.user_id_local
            else:
                raise ValidationError(
                    _("Case worker has no free occasions at that time.")
                )

    def _check_resource_calendar_date(self, check_date):
        """Checks if a date is overlapping with a holiday from resource.calender.leaves """
        res = (
            self.env["resource.calendar.leaves"]
            .sudo()
            .search_read(
                [("date_from", "<=", check_date), ("date_to", ">=", check_date)]
            )
        )
        if res:
            return False
        return True

    def start_meeting_search(self, type_id):
        days_first = self.type_id.days_first if self.type_id.days_first else 3
        # remove one day from start date since we add a day at the start of each loop.
        loop_start = datetime.now() - timedelta(days=1)
        i = 0

        while i < days_first:
            loop_start = loop_start + timedelta(days=1)
            if (
                loop_start.weekday() in [0, 1, 2, 3, 4]
            ) and self._check_resource_calendar_date(loop_start):
                i += 1

        return loop_start.replace(
            hour=BASE_DAY_START.hour,
            minute=BASE_DAY_START.minute,
            second=0,
            microsecond=0,
        )

    def stop_meeting_search(self, start_meeting_search, type_id):
        days_last = self.type_id.days_last if self.type_id.days_last else 15
        # remove one day from start date since we add a day at the start of each loop.
        loop_start = start_meeting_search - timedelta(days=1)
        i = 0

        while i < days_last:
            loop_start = loop_start + timedelta(days=1)
            if (
                loop_start.weekday() in [0, 1, 2, 3, 4]
            ) and self._check_resource_calendar_date(loop_start):
                i += 1

        return loop_start.replace(
            hour=BASE_DAY_STOP.hour,
            minute=BASE_DAY_STOP.minute,
            second=0,
            microsecond=0,
        )

    @api.one
    def inactivate(self, b=True):
        """Inactivates self. Used as a workaround to inactivate from server actions."""
        if b:
            self.active = False
        else:
            self.active = True
        return self.active

    def generate_cancel_daily_note(self, cancel_reason, appointment):
        pass

    def cancel(self, cancel_reason):
        """Cancels a planned meeting"""
        # Perform access control.
        if self.af_check_access():
            # Checks passed. Run inner function with sudo.
            return self.sudo()._cancel(cancel_reason)
        raise ValidationError(_("You are not allowed to cancel these meetings."))

    def _cancel(self, cancel_reason):
        # Do not allow cancellation of meetings that have been sent to ACE
        if not cancel_reason:
            return False
        for appointment in self:
            if appointment.state == "confirmed":
                appointment.state = "canceled"
                appointment.cancel_reason = cancel_reason.id

                self.generate_cancel_daily_note(cancel_reason, appointment)

                appointment.occasion_ids = [(5, 0, 0)]

                return True

    def confirm_appointment(self):
        """Confirm reserved booking"""
        # Perform access control.
        if self.af_check_access():
            # Checks passed. Run inner function with sudo.
            return self.sudo()._confirm_appointment()
        raise ValidationError(_("You are not allowed to confirm these meetings."))

    def _confirm_appointment(self):
        for appointment in self:
            if appointment.state == "reserved":
                appointment.state = "confirmed"

                res = True
            else:
                res = False

            return res

    @api.multi
    def write(self, vals):
        if (
            self.occasion_ids
            and (self.channel == self.env.ref("calendar_channel.channel_local"))
            and (vals.get("start") or vals.get("stop") or vals.get("type_id"))
        ):
            self._check_remaining_occasions()
        if vals.get("cancel_reason_temp"):
            vals["cancel_reason"] = vals.pop("cancel_reason_temp")
        res = super(CalendarAppointment, self).write(vals)
        return res

    @api.multi
    def _check_remaining_occasions(self):
        start_check = datetime.now() + timedelta(days=self.type_id.days_first)
        stop_check = datetime.now() + timedelta(days=self.type_id.days_last)
        min_num = (
            self.env["calendar.appointment.type.operation"]
            .sudo()
            .search(
                [
                    ("operation_id", "=", self.operation_id.id),
                    ("type_id", "=", self.type_id.id),
                ],
                limit=1,
            )
            .warning_threshold
        )

        if min_num:
            occ_num = self.env["calendar.occasion"].search_count(
                [
                    ("start", ">", start_check),
                    ("start", "<", stop_check),
                    ("type_id", "=", self.type_id.id),
                    ("additional_booking", "=", False),
                    ("appointment_id", "=", False),
                    ("state", "in", ["free", "confirmed"]),
                    ("operation_id", "=", self.operation_id.id),
                ]
            )

            if occ_num < min_num:
                if self.operation_id.app_warn_emp_ids:
                    for user in self.operation_id.app_warn_emp_ids:
                        template = self.env.ref(
                            "calendar_af.email_template_low_occasion_warning"
                        )
                        template.email_to = user.work_email
                        template.send_mail(self.id, force_send=True)
                else:
                    _logger.debug(
                        _("No threshold users setup for operation %s")
                        % self.operation_id.name
                    )
        else:
            _logger.debug(
                _("No threshold set for operation %s and meeting type %s")
                % (self.operation_id.name, self.type_id.name)
            )

    @api.multi
    def move_meeting_action(self):
        self.show_suggestion_ids = False
        partner = (
            self.env["calendar.appointment"]
            .browse(self._context.get("active_id"))
            .partner_id
        )
        return {
            "name": _("Move meeting"),
            "res_model": "calendar.move_appointment",
            "view_type": "form",
            "view_mode": "form",
            "view_id": self.env.ref("calendar_af.move_appointment_view_form").id,
            "target": "inline",
            "type": "ir.actions.act_window",
            "context": {},
        }

    @api.multi
    def cancel_meeting_action(self):
        partner = (
            self.env["calendar.appointment"]
            .browse(self._context.get("active_id"))
            .partner_id
        )
        return {
            "name": _("Cancel meeting"),
            "res_model": "calendar.cancel_appointment",
            "view_type": "form",
            "view_mode": "form",
            "view_id": self.env.ref("calendar_af.cancel_appointment_view_form").id,
            "target": "new",
            "type": "ir.actions.act_window",
            "context": {},
        }

    def generate_move_daily_note(self, occasions, reason):
        pass

    @api.one
    def move_appointment(self, occasions, reason=False):
        """ "Intended to be used to move appointments from one bookable occasion to another.
        :param occasions: a recordset of odoo occasions to move the meeting to."""
        res = False

        if occasions:
            # replace the occasions for the appointment
            vals = {
                "start": occasions[0].start,
                "stop": occasions[-1].stop,
                "duration": len(occasions) * BASE_DURATION / 60,
                "type_id": occasions[0].type_id.id,
                "additional_booking": False,
                "occasion_ids": [(6, 0, occasions._ids)],
            }
            self.write(vals)

            self.generate_move_daily_note(occasions, reason)
            res = True

        return res

    @api.model
    def delete_reservation(self, occasions):
        """Deletes a reservation
        :param occasions: a recordset of odoo occasions linked to a reservation"""
        reservation = (
            self.env["calendar.appointment"]
            .sudo()
            .search(
                [("occasion_ids", "in", occasions._ids), ("state", "=", "reserved")]
            )
        )
        if reservation:
            reservation.unlink()
            return True
        else:
            return False
