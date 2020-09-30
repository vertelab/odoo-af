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
    app_count = fields.Integer(string='Booked appointments', readonly=True)
    occ_count = fields.Integer(string='Possible appointments', readonly=True)
    add_book_count = fields.Integer(string='No. additional occasions', readonly=True)
    booked_from_cal = fields.Integer(string='Booked from calendar', readonly=True)
    free_occ = fields.Integer(string='Free occasions', readonly=True)
    no_overbooked = fields.Integer(string='Overbooked occasions', readonly=True)
    app_id = fields.Integer(string='Occasion id', readonly=True)
    user_id = fields.Many2one(comodel_name='res.users', string='Case worker', readonly=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Jobseeker', readonly=True)
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
    location = fields.Char(string='Location code', readonly=True)
    office_id = fields.Many2one(comodel_name='hr.department', string="Office", readonly=True)
    type_id = fields.Many2one(string='Type', comodel_name='calendar.appointment.type', readonly=True)
    additional_booking = fields.Boolean(String='Over booking', readonly=True)
    occ_start = fields.Datetime(string='Occasion start', readonly=True)
    occ_stop = fields.Datetime(string='Occasion stop', readonly=True)
    app_start = fields.Datetime(string='Appointment start', readonly=True)
    app_stop = fields.Datetime(string='Appointment stop', readonly=True)
    occ_start_time = fields.Char(string='Occasion start time', readonly=True)
    app_start_time = fields.Char(string='Appointment start time', readonly=True)

    def _select(self):
        select_str = """
             SELECT
                    COUNT(DISTINCT ca.id) as app_count,
                    COUNT(case co.additional_booking when 'f' then 1 else null end) as occ_count,
                    COUNT(case co.additional_booking when 't' then 1 else null end) as add_book_count,
                    COUNT(DISTINCT ca.id) - COUNT(case co.additional_booking when 't' then 1 else null end) as booked_from_cal,
                    COUNT(DISTINCT co.id) - COUNT(ca.id) as free_occ,
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
                    ca.location as location,
                    co.office_id as office_id,
                    co.type_id as type_id,
                    co.additional_booking as additional_booking,
                    ca.start as app_start,
                    ca.stop as app_stop,
                    ca.start_time as app_start_time,
                    co.start_time as occ_start_time
        """

        return select_str

    def _group_by(self):
        group_by_str = """
                GROUP BY
                    co.id,
                    ca.id,
                    co.start,
                    co.stop,
                    co.duration,
                    co.user_id,
                    ca.partner_id,
                    co.name,
                    co.state,
                    ca.state,
                    ca.location,
                    co.office_id,
                    co.type_id,
                    co.additional_booking,
                    ca.start,
                    ca.stop,
                    ca.start_time,
                    co.start_time
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
