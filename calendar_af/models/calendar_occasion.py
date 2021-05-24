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
from random import randint
from copy import copy

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from .calendar_constants import *

_logger = logging.getLogger(__name__)


class CalendarOccasion(models.Model):
    _name = "calendar.occasion"
    _description = "Occasion"

    name = fields.Char(string="Name", required=True)
    start = fields.Datetime(
        string="Start", required=True, help="Start date of an occasion", index=True
    )
    stop = fields.Datetime(
        string="Stop", required=True, help="Stop date of an occasion"
    )
    duration_selection = fields.Selection(
        string="Duration",
        selection=[("30 minutes", "30 minutes"), ("1 hour", "1 hour")],
    )
    duration = fields.Float("Duration")
    duration_text = fields.Char(
        "Duration", compute="_compute_duration_text", store=True
    )
    appointment_id = fields.Many2one(
        comodel_name="calendar.appointment", string="Appointment", index=True
    )
    type_id = fields.Many2one(
        comodel_name="calendar.appointment.type", string="Type", index=True
    )
    channel = fields.Many2one(
        string="Channel",
        comodel_name="calendar.channel",
        related="type_id.channel",
        readonly=True,
    )
    channel_name = fields.Char(
        string="Channel", related="type_id.channel.name", readonly=True
    )
    additional_booking = fields.Boolean(String="Over booking", index=True)
    user_id = fields.Many2one(
        string="Case worker",
        comodel_name="res.users",
        help="Booked case worker",
        index=True,
    )
    case_worker_name = fields.Char(
        string="Case worker", compute="_compute_case_worker_name", store=True
    )
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("request", "Published"),
            ("ok", "Accepted"),
            ("fail", "Rejected"),
            ("booked", "Booked"),
            ("deleted", "Deleted"),
        ],
        string="Occasion state",
        default="request",
        help="Status of the meeting",
        index=True,
    )
    operation_id = fields.Many2one(
        comodel_name="hr.operation", string="Operation", index=True
    )
    office_id = fields.Many2one(
        comodel_name="hr.department",
        string="Office",
        related="operation_id.department_id",
        readonly=True,
    )
    start_time = fields.Char(
        string="Occasion start time",
        readonly=True,
        compute="_occ_start_time_calc",
        store=True,
    )
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
    is_possible_start = fields.Selection(
        string="Is a possible start time",
        selection=[("", "Not set"), ("0", "No"), ("1", "Yes")],
    )
    # TODO: Couldn't we solve this with security rules?
    af_tree_filter = fields.Boolean(compute='_compute_af_tree_filter',
                                    search="_search_af_tree_filter",
                                    help="User dependant filtering for default tree view.")

    def _compute_af_tree_filter(self):
        """Not needed. We only use search."""
        pass

    @api.model
    def _search_af_tree_filter(self, op, value):
        """ Meeting Admin should see every occasion.
        Planners should only see their coworkers occasions.
        Regular users should only see their own occasions."""
        if op != "=":
            raise Warning(_("%s operator not implemented for calendar.occasion.af_tree_filter!") % op)
        if value is not True:
            raise Warning(_("Value '%s' not implemented for calendar.occasion.af_tree_filter!") % op)
        if self.env.user.has_group("base.group_system"):
            return []
        if self.env.user.has_group("af_security.af_meeting_admin"):
            return []
        if self.env.user.has_group("af_security.af_meeting_planner"):
            return [("user_id.employee_ids.operation_ids.id", "in", self.env.user.mapped("employee_ids.operation_ids.id"))]
        return [("user_id", "=", self.env.user.id)]

    @api.depends("duration")
    def _compute_duration_text(self):
        for rec in self:
            if rec.duration == 0.5:
                rec.duration_text = _("30 minutes")
            elif rec.duration == 1.0:
                rec.duration_text = _("1 hour")

    @api.one
    def _compute_weekday(self):
        if self.start:
            self.weekday = self.start.weekday()

    @api.one
    @api.depends("user_id")
    def _compute_case_worker_name(self):
        if self.channel == self.env.ref("calendar_channel.channel_pdm"):
            self.case_worker_name = _("Employment service officer")
        else:
            self.case_worker_name = f"{self.user_id.login} ({self.user_id.name})"

    @api.depends("start")
    def _occ_start_time_calc(self):
        offset = int(
            self[0]
            .start.astimezone(pytz.timezone(LOCAL_TZ))
            .utcoffset()
            .total_seconds()
            / 60
            / 60
        )
        for occ in self:
            occ.start_time = "%s:%s" % (
                str(occ.start.hour + offset).rjust(2, "0"),
                str(occ.start.minute).ljust(2, "0"),
            )

    @api.onchange("type_id")
    def set_duration_selection(self):
        self.name = self.type_id.name
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

    @api.model
    def _force_create_occasion(
        self,
        duration,
        start,
        type_id,
        channel,
        state,
        user=False,
        operation_id=False,
        additional_booking=True,
    ):
        """In case we need to force through a new occasion for some reason"""
        vals = {
            "name": _("%sm @ %s") % (duration, pytz.timezone(LOCAL_TZ).localize(start)),
            "start": start,
            "stop": start + timedelta(minutes=duration),
            "duration": duration,
            "appointment_id": False,
            "type_id": type_id,
            "channel": channel,
            "operation_id": operation_id.id if operation_id else False,
            "user_id": user.id if user else False,
            "additional_booking": additional_booking,
            "state": state,
        }
        res = self.env["calendar.occasion"].create(vals)
        return res

    @api.model
    def _get_min_occasions(self, type_id, date_start=None, date_stop=None):
        """Returns the timeslot (as a start date, DateTime) with the least
        amount of occurrences for a specific timeframe"""
        date_start = date_start or copy(BASE_DAY_START)
        # Additional occasions should not be created after 15:00
        date_stop = date_stop or copy(BASE_DAY_STOP)
        loop_date = date_start
        occ_time = {}
        while loop_date < date_stop:
            # do not check saturday or sunday
            # if loop_date.weekday() not in [5,6]:
            # make sure we don't book meetings during lunch (11:00-12:00)
            if (loop_date.hour != BASE_DAY_LUNCH.hour) and not (
                type_id.duration == 60
                and (
                    (
                        loop_date.hour == BASE_DAY_LUNCH.hour - 1
                        and loop_date.minute == 30
                    )
                    or (loop_date.hour == date_stop.hour - 1 and loop_date.minute == 30)
                )
            ):
                occ_time[loop_date.strftime("%Y-%m-%dT%H:%M:%S")] = self.env[
                    "calendar.occasion"
                ].search_count(
                    [("start", "=", loop_date), ("type_id", "=", type_id.id)]
                )
            loop_date = loop_date + timedelta(minutes=BASE_DURATION)
        occ_time_min_key = min(occ_time, key=occ_time.get)
        res = datetime.strptime(occ_time_min_key, "%Y-%m-%dT%H:%M:%S")
        return res

    @api.model
    def _check_date_mapping(self, date, operation_id=False):
        """Checks if a date has a mapped date, and returns the mapped date
        if it exists"""
        if operation_id:
            mapped_date = self.env["calendar.mapped_dates"].search(
                [("from_date", "=", date), ("operation_id", "=", operation_id.id)]
            )
        else:
            mapped_date = self.env["calendar.mapped_dates"].search(
                [("from_date", "=", date), ("operation_id", "=", False)]
            )
        if mapped_date:
            res = mapped_date.to_date
        else:
            res = date
        return res

    @api.model
    def _get_additional_booking(self, date, duration, type_id, operation_id=False):
        """ "Creates extra, additional, occasions. Iff overbooking is allowed.
        :param date: datetime object. Date to create occasion on.
        :param duration: Integer duration of the meeting in minutes.
        :param type_id: Object of type calendar.appointment.type.
        :param operation_id: Operation object, only used for non PDM.
        """
        user_id = False
        # Check if overbooking is allowed on this meeting type
        if not type_id.additional_booking:
            # TODO: Throw error instead?
            _logger.debug(_("Overbooking not allowed on %s" % type_id.name))
            return False
        # Replace date with mapped date if we have one
        date = self._check_date_mapping(date, operation_id)
        date_list = date.strftime("%Y-%-m-%-d").split("-")
        # Copy to make sure we dont overwrite BASE_DAY_START or BASE_DAY_STOP
        day_start = copy(BASE_DAY_START)
        day_stop = copy(BASE_DAY_STOP) - timedelta(hours=1)
        # Ugly, ugly code..
        day_start = day_start.replace(
            year=int(date_list[0]), month=int(date_list[1]), day=int(date_list[2])
        )
        day_stop = day_stop.replace(
            year=int(date_list[0]), month=int(date_list[1]), day=int(date_list[2])
        )
        res = self.env["calendar.occasion"]
        # Find when to create new occasion
        if (
            type_id.channel == self.env.ref("calendar_channel.channel_local")
            and operation_id
            and operation_id.reserve_time
        ):
            date_now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            datetime_offset = timedelta(
                days=type_id.days_last, hours=operation_id.reserve_time
            )
            start_date = date_now + datetime_offset
            # Calculate how many occasions we need
            if operation_id:
                if operation_id.reserve_admin_ids:
                    # find employees listed as available for reserve bookings on operation
                    employee_ids = operation_id.reserve_admin_ids
                    # select random employee from the recordset
                    user_id = employee_ids[randint(0, len(employee_ids) - 1)].user_id
                else:
                    # no user_id could be set.
                    raise ValidationError(
                        _("No case worker could be set for operation %s")
                        % operation_id.operation_code
                    )
        elif type_id.channel == self.env.ref("calendar_channel.channel_pdm"):
            if operation_id or user_id:
                raise ValidationError(
                    _(
                        "Trying to create an additional PDM occasion with operation_id or user_id."
                    )
                )
            # Additional booking for PDM
            start_date = self._get_min_occasions(type_id, day_start, day_stop)
        else:
            raise ValidationError(
                _("Could not create additional booking for operation %s")
                % operation_id.operation_code
                if operation_id.operation_code
                else operation_id
            )
        vals = {
            "name": "%sm @ %s" % (duration, start_date),
            "start": start_date,
            "stop": start_date + timedelta(minutes=duration),
            "duration": duration / 60,
            "appointment_id": False,
            "type_id": type_id.id,
            "channel": type_id.channel.id,
            "operation_id": operation_id.id if operation_id else False,
            "user_id": user_id.id if user_id else False,
            "additional_booking": True,
            "state": "ok",
        }
        res |= self.env["calendar.occasion"].create(vals)
        # TODO: use this method instead. Test before enabling.
        # res |= self._force_create_occasion(
        #     duration,
        #     start_date,
        #     type_id.id,
        #     type_id.channel.id,
        #     "ok",
        #     user_id.id if user_id else False,
        #     operation_id.id if operation_id else False,
        #     True,
        # )
        return res

    @api.multi
    def check_access_planner_locations(self, locations):
        """Check if current user is planner with access to these locations.
        :param locations: recordset of locations."""
        if not self.env.user.has_group("af_security.af_meeting_planner"):
            return False
        for occasion in self:
            # ensure that user has access to at least one location per occasion.
            if not occasion.mapped("office_id.operation_ids.location_id") & locations:
                return False
        return True

    @api.multi
    def af_check_access(self):
        """Perform access control before allowing certain operations.
        Controls access for:
        * publish_occasion
        * accept_occasion
        * reject_occasion
        * delete_occasion
        """
        allowed = False
        denied = False
        locations = self.env.user.mapped(
            "employee_ids.office_ids.operation_ids.location_id"
        )
        # Check access for Meeting Planner
        if self.check_access_planner_locations(locations):
            allowed = True
        if allowed and not denied:
            return True
        return False

    @api.multi
    def publish_occasion(self):
        """User publishes suggested occasion"""
        # Added this stop since we don't want to allow batch handling.
        for rec in self:
            if rec.state == "draft" or rec.state == "fail":
                # Perform access control.
                if rec.af_check_access():
                    # Checks passed. Run inner function with sudo.
                    res = rec.sudo()._publish_occasion()
                    if not res:
                        raise ValidationError(
                            _("One of your occasions is not a draft.")
                        )
                else:
                    raise ValidationError(
                        _("You are not allowed to publish these occasions.")
                    )
            else:
                raise ValidationError(
                    _("Only occasions in status Rejected or Draft can be published.")
                )

    @api.multi
    def _publish_occasion(self):
        if self.state == "draft" or self.state == "fail":
            self.state = "request"
            ret = True
        else:
            ret = False

        return ret

    @api.multi
    def accept_occasion(self):
        """User accepts suggested occasion"""
        # Added this stop since we don't want to allow batch handling.
        for rec in self:
            if rec.state == "request" or rec.state == "fail":
                # Perform access control.
                if rec.af_check_access():
                    # Checks passed. Run inner function with sudo.
                    res = rec.sudo()._accept_occasion()
                    if not res:
                        raise ValidationError(
                            _("One of your occasions is not a request.")
                        )
                else:
                    raise ValidationError(
                        _("You are not allowed to accept these occasions.")
                    )
            else:
                raise ValidationError(
                    _("Only occasions in status Rejected or Request can be accepted.")
                )

    def _accept_occasion(self):
        if self.state == "request" or self.state == "fail":
            self.state = "ok"
            ret = True
        else:
            ret = False

        return ret

    @api.multi
    def reject_occasion(self):
        """User rejects suggested occasion"""
        # Added this stop since we don't want to allow batch handling.
        for rec in self:
            if rec.state in ["request", "ok"]:
                # Perform access control.
                if rec.af_check_access():
                    # Checks passed. Run inner function with sudo.
                    res = rec.sudo()._reject_occasion()
                    if not res:
                        raise ValidationError(
                            _("One of your occasions is not a request.")
                        )
                else:
                    raise ValidationError(
                        _("You are not allowed to reject these occasions.")
                    )
            else:
                raise ValidationError(
                    _("Only occasions in status Accepted or Request can be rejected.")
                )

    @api.multi
    def _reject_occasion(self):
        if self.state in ["request", "ok"] and not self.appointment_id:
            self.state = "fail"
            ret = True
        else:
            ret = False

        return ret

    @api.multi
    def delete_occasion(self):
        """User deletes an occasion"""
        # Added this stop since we don't want to allow batch handling.
        for rec in self:
            if not rec.appointment_id:
                # Perform access control.
                if rec.af_check_access():
                    # Checks passed. Run inner function with sudo.
                    res = rec.sudo()._delete_occasion()
                    if not res:
                        raise ValidationError(
                            _("One of your occasions is already booked")
                        )
                else:
                    raise ValidationError(
                        _("You are not allowed to delete these occasions.")
                    )

    @api.multi
    def _delete_occasion(self):
        if not self.appointment_id:
            self.state = "deleted"
            ret = True
        else:
            ret = False

        return ret

    @api.model
    def get_bookable_occasions(
        self, start, stop, duration, type_id, operation_id=False, max_depth=1
    ):
        """Returns a list of occasions matching the defined parameters of the appointment. Creates additional
        occasions if allowed.
        :param start: Start search as this time.
        :param stop: Stop search as this time.
        :param duration: Meeting length.
        :param type_id: Meeting type.
        :param operation_id: The local office to filter for.
        :param max_depth: Number of bookable occasions per time slot.

        Pseudo-code:

        if 'local occasions':
            SQL query returns:

             user_id | start_date | start_time | array_agg
            ---------+------------+------------+-----------
             2       | 2020-11-25 | 09:00:00   | {210987}
             2       | 2020-11-25 | 09:30:00   | {210988}
             2       | 2020-11-25 | 13:00:00   | {210985}
             2       | 2020-11-25 | 13:30:00   | {210986}
             479     | 2020-11-25 | 13:00:00   | {210983}
             479     | 2020-11-25 | 13:30:00   | {210984}

            loop lines with respect to user and date in that order
                if meeting is more than 30 min long:
                    check if we allow meetings to be booked by comparing
                    number of occasions in previous loop with current.
                Add either max_depth or found # of allowed occasions to list occasions
                add list occasions to list occ_lists[index of date]
                repeat

        else 'pdm occasions':
            works the same as above but without users.
            SQL query returns:

             start_date | start_time |    array_agg
            ------------+------------+-----------------
             2020-11-25 | 09:00:00   | {210987}
             2020-11-25 | 09:30:00   | {210988}
             2020-11-25 | 13:00:00   | {210983,210985}
             2020-11-25 | 13:30:00   | {210984,210986}
             2020-11-20 | 13:00:00   | {210951}
             2020-11-20 | 13:30:00   | {210952}

        """

        # Calculate number of occasions needed to match booking duration
        date_delta = stop - start

        occ_lists = []
        # declare lists for each day
        for i in range(date_delta.days + 1):
            occ_lists.append([])

        sql_type_id = type_id.id
        sql_start = start
        sql_stop = stop

        # do search for local offices
        if (
            type_id.channel == self.env.ref("calendar_channel.channel_local")
            and operation_id
        ):
            # Specific variables for local offices
            sql_operation_id = operation_id.id

            sql_query = """SELECT user_id, start::date as start_date, start::time as start_time, array_agg(DISTINCT(id))
                            FROM calendar_occasion co
                            WHERE appointment_id IS NULL 
                                AND additional_booking = 'f'
                                AND type_id = %s
                                AND start >= %s
                                AND start <= %s
                                AND operation_id = %s
                                AND state = 'ok'
                            GROUP BY start::time, start::date, user_id
                            ORDER BY user_id ASC, start_date DESC, start_time ASC;"""
            # TODO: use %s in query and tuple with values as argument
            self._cr.execute(
                sql_query, (sql_type_id, sql_start, sql_stop, sql_operation_id)
            )
            sql_res = self._cr.fetchall()

            # handle 30 min meetings
            # if type_id.duration == 30:
            # this is default behaviour now.
            prev_user_id = False
            prev_date = False
            day_num = 0
            for dt_occ_pair in sql_res:
                curr_user_id = dt_occ_pair[0]
                curr_date = dt_occ_pair[1]
                curr_starts = dt_occ_pair[3]
                if not prev_date:
                    prev_date = curr_date
                    prev_user_id = curr_user_id
                if curr_user_id != prev_user_id:
                    day_num = 0
                    prev_date = curr_date
                    prev_user_id = curr_user_id
                if curr_date != prev_date:
                    day_num += 1
                occasions = []
                if len(occ_lists[day_num]) < max_depth:
                    for i in range(min(max_depth, len(curr_starts))):
                        occ_id = self.env["calendar.occasion"].browse(curr_starts[i])
                        occasions.append(occ_id)
                occ_lists[day_num].append(occasions)
                prev_date = curr_date
                prev_user_id = curr_user_id
        # Do PDM search
        else:
            sql_query = """SELECT start::date as start_date, start::time as start_time, array_agg(id)
                            FROM calendar_occasion
                            WHERE appointment_id IS NULL
                                AND additional_booking = 'f' 
                                AND type_id = %s
                                AND start >= %s
                                AND start <= %s
                                AND state = 'ok'
                            GROUP BY start::time, start::date
                            ORDER BY start_date DESC, start_time ASC;"""
            self._cr.execute(sql_query, (sql_type_id, sql_start, sql_stop))
            sql_res = self._cr.fetchall()

            # PDM meetings only need 1 occasion with same duration
            # as appointment regardless of duration.
            # Run similar logic as for 30 min local meetings.
            prev_date = False
            day_num = 0
            for dt_occ_pair in sql_res:
                curr_date = dt_occ_pair[0]
                curr_starts = dt_occ_pair[2]
                if not prev_date:
                    prev_date = curr_date
                if curr_date != prev_date:
                    day_num = +1
                occasions = []
                for i in range(min(max_depth, len(curr_starts))):
                    occ_id = self.env["calendar.occasion"].browse(curr_starts[i])
                    occasions.append(occ_id)
                occ_lists[day_num].append(occasions)
                prev_date = curr_date

        # if type allows additional bookings and we didn't find any
        # free occasions, create new ones:
        if type_id.additional_booking and all(not l for l in occ_lists):
            # Changed this line to create over bookings on the LAST allowed date.
            occ_lists[-1].append(
                [self._get_additional_booking(stop, duration, type_id, operation_id)]
            )

        return occ_lists

    @api.model
    def reserve_occasion(self, occasion_ids):
        """Reserves an occasion.
        :param occasion_ids: Recordset of calendar.occasion objects."""
        start = occasion_ids[0].start
        stop = occasion_ids[len(occasion_ids) - 1].stop
        duration = (stop - start).seconds / 60 / 60
        type_id = occasion_ids[0].type_id

        # check that occasions are free and unreserved
        free = True
        for occasion_id in occasion_ids:
            if (
                occasion_id.appointment_id
                and occasion_id.appointment_id.state != "reserved"
            ) or (
                occasion_id.appointment_id
                and occasion_id.appointment_id.state == "reserved"
                and occasion_id.appointment_id.reserved
                > datetime.now() - timedelta(seconds=RESERVED_TIMEOUT)
            ):
                free = False

        if free:
            vals = {
                "name": type_id.name,
                "start": start,
                "stop": stop,
                "duration": duration,
                "type_id": type_id.id,
                "user_id": False,
                "partner_id": False,
                "state": "reserved",
                "operation_id": False,
                "occasion_ids": occasion_ids,  # I dont think this does anything?
                "reserved": datetime.now(),
            }
            appointment = self.env["calendar.appointment"].create(vals)

            # relation needs to be set from calendar.occasion?
            for occasion_id in occasion_ids:
                occasion_id.appointment_id = appointment.id

            res = appointment
        else:
            res = False

        return res

    @api.model
    def autovacuum_additional_occasion(self):
        """Called from scheduled action to clear system of unused
        additional occasions"""
        del_occ = (
            self.env["calendar.occasion"]
            .sudo()
            .search([("additional_booking", "=", True), ("appointment_id", "=", False)])
        )
        _logger.debug("Removing the following additional occasions: %s" % del_occ)
        del_occ.unlink()
