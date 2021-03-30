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

import copy
import logging
from datetime import timedelta

from odoo import models, fields, api, _

from .calendar_constants import *

_logger = logging.getLogger(__name__)


class CalendarSchedule(models.Model):
    _name = "calendar.schedule"
    _description = "Schedule"

    name = fields.Char(string="Name", required=True)
    start = fields.Datetime(
        string="Start", required=True, help="Start date of a schedule"
    )
    stop = fields.Datetime(string="Stop", required=True, help="Stop date of a schedule")
    duration = fields.Float("Duration")
    scheduled_agents = fields.Integer(
        string="Scheduled agents", help="Number of scheduled agents"
    )
    forecasted_agents = fields.Integer(
        string="Forecasted agents", help="Number of forecasted agents"
    )
    type_id = fields.Many2one(
        string="Meeting type",
        comodel_name="calendar.appointment.type",
        help="Related meeting type",
    )
    channel = fields.Many2one(string="Channel", comodel_name="calendar.channel")
    active = fields.Boolean(string="Active", default=True)

    @api.one
    def inactivate(self, b=True):
        """Inactivates self. Used as a workaround to inactivate from server actions."""
        if b:
            self.active = False
        else:
            self.active = True
        return self.active

    @api.multi
    def create_occasions(self):
        """Creates a number of occasions from schedules, depending on
        number of scheduled agents"""

        for schedule in self:
            duration = schedule.type_id.duration / 60.0
            stop = schedule.start + timedelta(minutes=schedule.type_id.duration)

            no_occasions = self.env["calendar.occasion"].search_count(
                [
                    ("start", "=", schedule.start),
                    ("type_id", "=", schedule.type_id.id),
                    ("additional_booking", "=", False),
                    ("state", "=", "ok"),
                ]
            )
            if schedule.type_id.channel == self.env.ref("calendar_channel.channel_local"):
                occasions_delta = schedule.scheduled_agents - no_occasions
            elif schedule.type_id.channel == self.env.ref("calendar_channel.channel_pdm"):
                occasions_delta = schedule.forecasted_agents - no_occasions
            else:
                occasions_delta = 0
                _logger.warning(
                    _(
                        "Unhandled meeting type while creating occasions from schedules: %s"
                    )
                    % schedule.type_id
                )
            if occasions_delta > 0:
                vals = {
                    "name": _("%sm @ %s")
                    % (
                        schedule.type_id.duration,
                        pytz.timezone(LOCAL_TZ).localize(schedule.start),
                    ),
                    "duration": duration,
                    "start": schedule.start,
                    "stop": stop,
                    "type_id": schedule.type_id.id,
                    "channel": schedule.channel,
                    "additional_booking": False,
                    "state": "ok",
                }
                # get booked additional occasions
                no_occasions_add = self.env["calendar.occasion"].search_count(
                    [
                        ("start", "=", schedule.start),
                        ("type_id", "=", schedule.type_id.id),
                        ("additional_booking", "=", True),
                        ("appointment_id", "!=", False),
                        ("state", "=", "ok"),
                    ]
                )
                # Consider reserve bookings before creating new occasions
                for occasion in range(occasions_delta - no_occasions_add):
                    self.env["calendar.occasion"].create(vals)

            elif occasions_delta < 0:
                occ_del = self.env["calendar.occasion"].search(
                    [
                        ("start", "=", schedule.start),
                        ("type_id", "=", schedule.type_id.id),
                        ("additional_booking", "=", False),
                        ("appointment_id", "=", False),
                        ("state", "=", "ok"),
                    ],
                    limit=-occasions_delta,
                )
                # batch delete all 'extra' occasions
                occ_del.sudo().write({"state": "deleted"})

        # recalculate possible start times
        self.sudo().comp_possible_starts()

    @api.multi
    def comp_possible_starts(self):
        """Updates possible start times for appointments
        on a given day and meeting type

        I will leave this SQL here in case we want to use it in the future.
        For now I'm not implementing it since in my early tests the gain
        from implementing it seemed marginal in this case.

        SELECT start,COUNT(id)
        FROM calendar_occasion
        WHERE type_id = 2
            AND start >= '2020-11-18 00:00:01'
            AND start <= '2020-11-18 23:59:59'
            AND state = 'ok'
            AND appointment_id IS NULL
        GROUP BY start ORDER BY start ASC;

                start        | count
        ---------------------+-------
         2020-11-18 08:00:00 |   217
         2020-11-18 08:30:00 |   226
         2020-11-18 09:00:00 |   222
         2020-11-18 09:30:00 |   223
         2020-11-18 10:00:00 |   208
         2020-11-18 11:30:00 |    74
         2020-11-18 12:00:00 |   145
         2020-11-18 12:30:00 |   177
         2020-11-18 13:00:00 |   180
         2020-11-18 13:30:00 |   190
         2020-11-18 14:00:00 |   186

        SELECT start,array_agg(DISTINCT(id))
        FROM calendar_occasion
        WHERE type_id = 2
            AND start >= '2020-11-18 00:00:01'
            AND start <= '2020-11-18 23:59:59'
            AND state = 'ok'
            AND appointment_id IS NULL
        GROUP BY start ORDER BY start ASC;

        returns a list of ids instead of COUNT(id)

        """

        if self.type_id.channel == self.env.ref("calendar_channel.channel_pdm"):
            # do not run for PDM-meetings for now.
            # PDM meetings will now have 1 occasion per appointment
            # with the same length. 1 = pdm occasion = one free start.
            return

        # init start date and time
        loop_date = copy.copy(BASE_DAY_START).replace(
            year=self.start.year, month=self.start.month, day=self.start.day
        )

        # init last_dict and set all previous values to 0 since this is the first loop
        last_dict = {}

        # 16 is the number of half/whole hour slots between 9 and 17. Hopefully.
        for j in range(16):
            search_domain = [
                ("type_id", "=", self.type_id.id),
                ("start", "=", loop_date),
                ("state", "=", "ok"),
                ("appointment_id", "=", False),
            ]
            if self.type_id.duration == 60:
                no_occasions = self.env["calendar.occasion"].search_count(search_domain)
                # compute possible appointment starts for this time and type
                no_possible_starts = max(
                    no_occasions - last_dict.get(self.type_id.id, 0), 0
                )
                # update last_dict for appointment type
                last_dict[self.type_id.id] = no_possible_starts

                if no_possible_starts != 0:
                    occasions_true = self.env["calendar.occasion"].search(
                        search_domain, limit=no_possible_starts
                    )
                    occasions_false = self.env["calendar.occasion"].search(
                        search_domain + [("id", "not in", occasions_true._ids)],
                        limit=no_possible_starts,
                    )
                    occasions_true.write({"is_possible_start": "1"})
                    occasions_false.write({"is_possible_start": "0"})
            else:
                # if 30 min meeting length all occs are possible starts
                occasions_true = self.env["calendar.occasion"].search(search_domain)
                occasions_true.write({"is_possible_start": "1"})

            # move ahead by 30 mins
            loop_date += timedelta(minutes=BASE_DURATION)

    @api.model
    def cron_get_schedules(self, type_ids, days):

        _logger.debug(
            "Starting cron_get_schedules for meeting types: %s at %s"
            % (type_ids, datetime.now())
        )
        route = self.env.ref("edi_af_appointment.schedule")
        cal_schedule_ids = self.env["calendar.schedule"]
        days -= 1

        def _create_message(mes_start, mes_stop):
            vals = {
                "name": "IPF request",
                "start": mes_start,
                "stop": mes_stop,
                "type_id": type_id.id,
            }
            cal_schedule = self.env["calendar.schedule"].create(vals)

            vals = {
                "name": "Schedule request",
                "edi_type": self.env.ref("edi_af_appointment.appointment_schedules").id,
                "model": cal_schedule._name,
                "res_id": cal_schedule.id,
                "route_id": route.id,
                "route_type": "edi_af_schedules",
            }
            msg = self.env["edi.message"].create(vals)
            msg.pack()
            return cal_schedule

        for type_id in type_ids:
            start = datetime.now()
            # if we request more than 30 days, split the requests
            if days <= 30:
                cal_schedule_ids |= _create_message(start, start + timedelta(days=days))
            else:
                i = 0
                # int() will always round down
                loop_times = int(days / 30)
                while i <= loop_times:
                    # handle last loop different
                    if i == loop_times:
                        cal_schedule_ids |= _create_message(
                            start + timedelta(days=(30 * i)),
                            start + timedelta(days=days),
                        )
                    else:
                        cal_schedule_ids |= _create_message(
                            start + timedelta(days=(30 * i)),
                            start + timedelta(days=(30 * (i + 1))),
                        )

                    i += 1

        # force a commit in order to save the messages before processing
        self.env.cr.commit()
        route.run()
        cal_schedule_ids.inactivate()
        self.env.cr.commit()
        _logger.debug(
            "Completed cron_get_schedules for meeting types: %s at %s"
            % (type_ids, datetime.now())
        )
