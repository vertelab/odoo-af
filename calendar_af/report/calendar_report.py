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

class CalendarAppointmentReport(models.Model):
    _name = 'report.calendar.appointment'
    _description = "Appointment report"
    _order = 'name'
    _auto = False

    name = fields.Char(string='Name', readonly=True)
    duration = fields.Float(string='Duration', readonly=True)
    user_id = fields.Many2one(comodel_name='res.users', string='Case worker', readonly=True)
    partner_id = fields.Many2one(comodel_name='res.users', string='Case worker', readonly=True)
    app_state = fields.Selection(selection=[('free', 'Draft'),
                                        ('reserved', 'Reserved'),
                                        ('confirmed', 'Confirmed'),
                                        ('done', 'Done'),
                                        ('canceled', 'Canceled')],
                                        string='State', 
                                        help="Status of the meeting",
                                        readonly=True)
    occ_state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('request', 'Published'),
                                        ('ok', 'Accepted'),
                                        ('fail', 'Rejected')],
                                        string='Occasion state', 
                                        help="Status of the meeting",
                                        readonly=True)
    location_code = fields.Char(string='Location code', readonly=True)
    office = fields.Many2one(comodel_name='res.partner', string="Office", readonly=True)
    type_id = fields.Many2one(string='Type', comodel_name='calendar.appointment.type', readonly=True)
    additional_booking = fields.Boolean(String='Over booking', readonly=True)
    occ_start = fields.Datetime(string='Occasion start', readonly=True)
    occ_stop = fields.Datetime(string='Occasion stop', readonly=True)
    app_start = fields.Datetime(string='Appointment start', readonly=True)
    app_stop = fields.Datetime(string='Appointment stop', readonly=True)
    occ_start_time = fields.Char(string='Occasion start time', readonly=True)
    app_start_time = fields.Char(string='Appointment start time', readonly=True)
    
    # app_datetime = fields.Datetime(string='Scheduled Agents', readonly=True)
    # week_num = fields.Char(string='Scheduled Agents', readonly=True)
    # scheduled_agents = fields.Integer(string='Scheduled Agents', readonly=True)
    # booked_apps_total = fields.Integer(string='Total booked appointments', readonly=True)
    # additional_bookings = fields.Integer(string='Additional bookings', readonly=True)
    # booked_ordinary_apps = fields.Integer(string='Booked ordinary appointments', readonly=True)
    # free_occasions = fields.Integer(string='Free occasions', readonly=True)
    # overbooking = fields.Integer(string='Overbooking', readonly=True)
    
    def _select(self):
        select_str = """
             SELECT
                    (select 1 ) AS nbr,
                    co.id as id,
                    co.start as occ_start,
                    co.stop as occ_stop,
                    co.duration as duration,
                    co.user_id as user_id,
                    ca.partner_id as partner_id,
                    co.name as name,
                    co.state as occ_state,
                    ca.state as app_state,
                    ca.location_code as location_code,
                    co.office as office,
                    co.type_id as type_id,
                    co.additional_booking as additional_booking,
                    ca.start as app_start,
                    ca.stop as app_stop,
                    CONCAT(CAST(EXTRACT(HOUR FROM co.start) AS varchar),':',CAST(EXTRACT(MINUTE FROM co.start) AS varchar)) as occ_start_time,
                    CONCAT(CAST(EXTRACT(HOUR FROM ca.start) AS varchar),':',CAST(EXTRACT(MINUTE FROM ca.start) AS varchar)) as app_start_time
        """
        # (extract('epoch' from (t.date_deadline-(now() at time zone 'UTC'))))/(3600*24)  as delay_endings_days
        return select_str

    def _group_by(self):
        group_by_str = """
                GROUP BY
                    co.id,
                    co.start,
                    co.stop,
                    co.duration,
                    co.user_id,
                    ca.partner_id,
                    co.name,
                    co.state,
                    ca.state,
                    ca.location_code,
                    co.office,
                    co.type_id,
                    co.additional_booking,
                    ca.start,
                    ca.stop
        """
        return group_by_str

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE view %s as
              %s
              FROM calendar_occasion co
                LEFT JOIN calendar_appointment ca ON ca.id = co.appointment_id
                    %s
        """ % (self._table, self._select(), self._group_by()))



        # """
        # select * from calendar_occasion co
        # LEFT JOIN calendar_appointment ca ON ca.id = co.appointment_id
        # """

        # self._cr.execute("""
        #     CREATE view %s as
        #       %s
        #       FROM calendar_occasion co
        #         LEFT JOIN calendar_appointment ca ON ca.id = co.appointment_id
        #             WHERE t.active = 'true'
        #             %s
        # """ % (self._table, self._select(), self._group_by()))