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

from odoo import models, fields, api, _, tools
from datetime import datetime, timedelta
from copy import copy
import pytz
import logging

_logger = logging.getLogger(__name__)

# LOCAL_TZ: Local timezone
LOCAL_TZ = "Europe/Stockholm"
# BASE_DURATION: Base duration given by TeleOpti. This is the duration of the calendar.schedule slots in minutes.
BASE_DURATION = 30.0
# BASE_DAY_START, BASE_DAY_STOP: The hours between which we normally accept appointments
BASE_DAY_START = (
    pytz.timezone(LOCAL_TZ)
    .localize(datetime.now().replace(hour=9, minute=0, second=0, microsecond=0))
    .astimezone(pytz.utc)
)
BASE_DAY_STOP = (
    pytz.timezone(LOCAL_TZ)
    .localize(datetime.now().replace(hour=16, minute=0, second=0, microsecond=0))
    .astimezone(pytz.utc)
)




class CalendarAppointmentReport(models.Model):
    _name = "report.calendar.appointment"
    _description = "Appointment report"
    _order = "name"
    _auto = False

    name = fields.Char(string="Name", readonly=True)
    duration = fields.Float(string="Duration", readonly=True)
    app_count = fields.Integer(string="Booked appointments", readonly=True)
    occ_count = fields.Integer(string="Possible appointments", readonly=True)
    add_book_count = fields.Integer(string="No. additional occasions", readonly=True)
    booked_from_cal = fields.Integer(string="Booked from calendar", readonly=True)
    free_occ = fields.Integer(string="Free occasions", readonly=True)
    no_overbooked = fields.Integer(string="Overbooked occasions", readonly=True)
    app_id = fields.Integer(string="Occasion id", readonly=True)
    user_id = fields.Many2one(
        comodel_name="res.users", string="Case worker", readonly=True
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Jobseeker", readonly=True
    )
    app_state = fields.Selection(
        selection=[
            ("free", "Draft"),
            ("reserved", "Reserved"),
            ("confirmed", "Confirmed"),
            ("done", "Done"),
            ("canceled", "Canceled"),
        ],
        string="State",
        help="Status of the meeting",
        readonly=True,
    )
    occ_state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("request", "Published"),
            ("ok", "Accepted"),
            ("fail", "Rejected"),
            ("deleted", "Deleted"),
        ],
        string="Occasion state",
        help="Status of the meeting",
        readonly=True,
    )
    operation_id = fields.Many2one(
        string="Operation", comodel_name="hr.operation", readonly=True
    )
    type_id = fields.Many2one(
        string="Type", comodel_name="calendar.appointment.type", readonly=True
    )
    additional_booking = fields.Boolean(String="Over booking", readonly=True)
    occ_start = fields.Datetime(string="Occasion start", readonly=True)
    occ_stop = fields.Datetime(string="Occasion stop", readonly=True)
    app_start = fields.Datetime(string="Appointment start", readonly=True)
    app_stop = fields.Datetime(string="Appointment stop", readonly=True)
    occ_start_time = fields.Char(string="Occasion start time", readonly=True)
    app_start_time = fields.Char(string="Appointment start time", readonly=True)

    def _select(self):
        select_str = """
             SELECT
                COUNT(DISTINCT distinct_co.app_id) as app_count,
                COUNT(co.id) as occ_count,
                COUNT(case co.additional_booking when 't' then 1 else null end) as add_book_count,
                COUNT(DISTINCT ca.id) - COUNT(case co.additional_booking when 't' then 1 else null end) as booked_from_cal,
                (case is_possible_start when '1' then 1 else 0 end) - COUNT(ca.id) as free_occ,
                case when COUNT(case co.additional_booking when 'f' then 1 else null end) - COUNT(ca.id) > 0 then 0 else -(COUNT(case co.additional_booking when 'f' then 1 else null end) - COUNT(ca.id)) end as no_overbooked,
                co.id as id,
                ca.id as app_id,
                co.start as occ_start,
                co.stop as occ_stop,
                co.duration as duration,
                co.user_id as user_id,
                ca.partner_id as partner_id,
                co.name as name,
                co.state as occ_state,
                ca.state as app_state,
                ca.operation_id as operation_id,
                co.type_id as type_id,
                co.additional_booking as additional_booking,
                ca.start as app_start,
                ca.stop as app_stop,
                ca.start_time as app_start_time,
                co.start_time as occ_start_time
        """
        #
        return select_str

    def _group_by(self):
        group_by_str = """
                GROUP BY
                    co.id,
                    ca.id,
                    co.start,
                    co.duration,
                    co.user_id,
                    ca.partner_id,
                    co.name,
                    co.state,
                    ca.state,
                    ca.operation_id,
                    co.operation_id,
                    co.type_id,
                    co.additional_booking,
                    ca.start,
                    ca.start_time,
                    co.start_time
        """
        #
        return group_by_str

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute(
            """
            CREATE view %s as
              %s
              FROM calendar_occasion co
                LEFT JOIN calendar_appointment ca 
                    ON ca.id = co.appointment_id
                LEFT JOIN (
                    SELECT DISTINCT(appointment_id) app_id, MIN(id) id 
                    FROM calendar_occasion 
                    WHERE appointment_id IS NOT NULL 
                    GROUP BY appointment_id
                    ) as distinct_co 
                    ON co.id = distinct_co.id
                LEFT JOIN calendar_appointment_type cat
                    on co.type_id = cat.id
              WHERE cat.channel = %s 
              %s
        """
            % (self._table, self._select(), self.env.ref("calendar_channel.channel_pdm").id, self._group_by())
        )

    @api.model
    def comp_possible_starts(self, start=datetime.now(), days_ahead=30):
        """ This method is currently not in use. It's intented to be used
            in connection with server actions to debug or similar.
            
            comp_possible_starts() on model calendar.schedule as defined 
            in calendar_af module is used instead.
        """
        app_types = self.env["calendar.appointment.type"].search(
            [("channel", "=", self.env.ref("calendar_channel.channel_pdm").id)]
        )

        # init start date and time
        loop_date = copy(BASE_DAY_START).replace(
            year=start.year, month=start.month, day=start.day
        )

        # init last_dict and set all previous values to 0 since this is the first loop
        last_dict = {}

        # look days_ahead number of days ahead
        for i in range(days_ahead):
            # 16 is the number of half/whole hour slots between 9 and 17. Hopefully.
            for j in range(16):
                for app_type in app_types:
                    search_domain = [
                        ("type_id", "=", app_type.id),
                        ("start", "=", loop_date),
                        ("state", "=", "ok"),
                        ("appointment_id", "=", False),
                    ]
                    if app_type.duration == 60:
                        no_occasions = self.env["calendar.occasion"].search_count(
                            search_domain
                        )
                        # compute possible appointment starts for this time and type
                        no_possible_starts = max(
                            no_occasions - last_dict.get(app_type.id, 0), 0
                        )
                        # update last_dict for appointment type
                        last_dict[app_type.id] = no_possible_starts

                        if no_possible_starts != 0:
                            occasions_true = self.env["calendar.occasion"].search(
                                search_domain, limit=no_possible_starts
                            )
                            occasions_false = self.env["calendar.occasion"].search(
                                search_domain + [("id", "not in", occasions_true._ids)],
                                limit=no_possible_starts,
                            )
                            for occ_true in occasions_true:
                                occ_true.is_possible_start = "1"
                            for occ_false in occasions_false:
                                occ_false.is_possible_start = "0"
                    else:
                        # if 30 min meeting length all occs are possible starts
                        occasions_true = self.env["calendar.occasion"].search(
                            search_domain
                        )
                        for occ_true in occasions_true:
                            occ_true.is_possible_start = "1"

                # move ahead by 30 mins
                loop_date += timedelta(minutes=BASE_DURATION)
            # move ahead 1 day and reset to start time.
            loop_date += timedelta(days=1, hours=-8)
