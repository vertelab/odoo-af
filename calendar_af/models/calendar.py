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
from random import randint
from datetime import datetime, timedelta, date
from odoo.exceptions import Warning

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

# TODO: decide if we are dependent on this variable or the imported schedule duration.
# LOCAL_TZ: Local timezone 
LOCAL_TZ = 'Europe/Stockholm'
# BASE_DURATION: Base duration given by TeleOpti. This is the duration of the calendar.schedule slots in minutes.
BASE_DURATION = 30.0
# BASE_DAY_START, BASE_DAY_STOP: The hours between which we normally accept appointments
BASE_DAY_START = pytz.timezone(LOCAL_TZ).localize(
    datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)).astimezone(pytz.utc)
BASE_DAY_STOP = pytz.timezone(LOCAL_TZ).localize(
    datetime.now().replace(hour=16, minute=0, second=0, microsecond=0)).astimezone(pytz.utc)
BASE_DAY_LUNCH = pytz.timezone(LOCAL_TZ).localize(
    datetime.now().replace(hour=11, minute=0, second=0, microsecond=0)).astimezone(pytz.utc)
# RESERVED_TIMEOUT is the default time before a reservation times out.
RESERVED_TIMEOUT = 300.0


# Termer
# appointment = faktiskt bokat möte
# occasions = bokningsbara tider
# schedule = occasions skapas utifrån informationen schedules

class CalendarSchedule(models.Model):
    _name = 'calendar.schedule'
    _description = "Schedule"

    name = fields.Char(string='Name', required=True)
    start = fields.Datetime(string='Start', required=True, help="Start date of a schedule")
    stop = fields.Datetime(string='Stop', required=True, help="Stop date of a schedule")
    duration = fields.Float('Duration')
    scheduled_agents = fields.Integer(string='Scheduled agents', help="Number of scheduled agents")
    forecasted_agents = fields.Integer(string='Forecasted agents', help="Number of forecasted agents")
    type_id = fields.Many2one(string='Meeting type', comodel_name='calendar.appointment.type',
                              help="Related meeting type")
    channel = fields.Many2one(string='Channel', comodel_name='calendar.channel')
    active = fields.Boolean(string='Active', default=True)

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
            no_occasions = self.env["calendar.occasion"].search_count(
                [
                    ("start", "=", schedule.start),
                    ("type_id", "=", schedule.type_id.id),
                    ("additional_booking", "=", False),
                    ("state", "=", "ok"),
                ]
            )
            occasions_delta = schedule.scheduled_agents - no_occasions
            if occasions_delta > 0:
                vals = {
                    "name": _("%sm @ %s")
                    % (
                        schedule.duration,
                        pytz.timezone(LOCAL_TZ).localize(schedule.start),
                    ),
                    "duration": schedule.duration,
                    "start": schedule.start,
                    "stop": schedule.stop,
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

        # init start date and time
        loop_date = copy.copy(BASE_DAY_START).replace(
            year=self.start.year, month=self.start.month, day=self.start.day)

        # init last_dict and set all previous values to 0 since this is the first loop
        last_dict = {}

        # 16 is the number of half/whole hour slots between 9 and 17. Hopefully.
        for j in range(16):
            search_domain = [('type_id', '=', self.type_id.id), ('start', '=', loop_date), ('state', '=', 'ok'), ('appointment_id', '=', False)]
            if self.type_id.duration == 60:
                no_occasions = self.env['calendar.occasion'].search_count(search_domain)
                # compute possible appointment starts for this time and type
                no_possible_starts = max(no_occasions - last_dict.get(self.type_id.id, 0), 0)
                # update last_dict for appointment type
                last_dict[self.type_id.id] = no_possible_starts

                if no_possible_starts != 0:
                    occasions_true = self.env['calendar.occasion'].search(search_domain, limit=no_possible_starts)
                    occasions_false = self.env['calendar.occasion'].search(search_domain + [('id', 'not in', occasions_true._ids)], limit=no_possible_starts)
                    occasions_true.write({'is_possible_start': '1'})
                    occasions_false.write({'is_possible_start': '0'})
            else:
                # if 30 min meeting length all occs are possible starts
                occasions_true = self.env['calendar.occasion'].search(search_domain)
                occasions_true.write({'is_possible_start': '1'})

            # move ahead by 30 mins
            loop_date += timedelta(minutes=BASE_DURATION)

    @api.model
    def cron_get_schedules(self, type_ids, days):

        _logger.debug("Starting cron_get_schedules for meeting types: %s at %s" % (type_ids, datetime.now()))
        route = self.env.ref('edi_af_appointment.schedule')
        cal_schedule_ids = self.env['calendar.schedule']
        days -= 1

        def _create_message(mes_start, mes_stop):
            vals = {
                'name': "IPF request",
                'start': mes_start,
                'stop': mes_stop,
                'type_id': type_id.id,
            }
            cal_schedule = self.env['calendar.schedule'].create(vals)

            vals = {
                'name': 'Schedule request',
                'edi_type': self.env.ref('edi_af_appointment.appointment_schedules').id,
                'model': cal_schedule._name,
                'res_id': cal_schedule.id,
                'route_id': route.id,
                'route_type': 'edi_af_schedules',
            }
            msg = self.env['edi.message'].create(vals)
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
                        cal_schedule_ids |= _create_message(start + timedelta(days=(30 * i)),
                                                            start + timedelta(days=days))
                    else:
                        cal_schedule_ids |= _create_message(start + timedelta(days=(30 * i)),
                                                            start + timedelta(days=(30 * (i + 1))))

                    i += 1

        # force a commit in order to save the messages before processing
        self.env.cr.commit()
        route.run()
        cal_schedule_ids.inactivate()
        self.env.cr.commit()
        _logger.debug("Completed cron_get_schedules for meeting types: %s at %s" % (type_ids, datetime.now()))


class CalendarAppointmentType(models.Model):
    _name = 'calendar.appointment.type'
    _description = "Meeting type"
    _order = 'ipf_num'

    name = fields.Char('Meeting type name', required=True)
    ipf_id = fields.Char('Teleopti competence id', required=True,
                         help="The IPF type id, if this is wrong the integration won't work")
    ipf_name = fields.Char('Teleopti competence name')
    channel = fields.Many2one(string='Channel', comodel_name='calendar.channel')
    duration = fields.Float(string='Duration', compute='_comp_duration', store=True)
    duration_30 = fields.Boolean(string='30 min')
    duration_60 = fields.Boolean(string='60 min')
    days_first = fields.Integer(string='First allowed day for type')
    days_last = fields.Integer(string='Last allowed day for type')
    ipf_num = fields.Integer(string='Meeting type id')
    additional_booking = fields.Boolean(string='Over booking')
    text = fields.Text(string='Comment')
    skill_ids = fields.Many2many(comodel_name='hr.skill', string='Skills')

    @api.depends('duration_30', 'duration_60')
    def _comp_duration(self):
        for channel in self:
            channel.duration = 30.0 if channel.duration_30 else 60.0


class CalendarChannel(models.Model):
    _name = 'calendar.channel'
    _description = "Channel"

    name = fields.Char('Name', translate=True, required=True )


class CalendarMappedDates(models.Model):
    _name = 'calendar.mapped_dates'
    _description = "Mapped dates"

    name = fields.Char(string="Name")
    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    operation_id = fields.Many2one(comodel_name='hr.operation', string='Operation')


class CalendarAppointmentSuggestion(models.Model):
    _name = 'calendar.appointment.suggestion'
    _description = "Bookable Occasion"

    appointment_id = fields.Many2one(comodel_name='calendar.appointment', ondelete='cascade')
    start = fields.Datetime()
    stop = fields.Datetime()
    duration = fields.Float(string='Duration')
    duration_text = fields.Char(string="Duration", compute="compute_duration_text")
    occasion_ids = fields.Many2many(comodel_name='calendar.occasion', string="Occasions")
    type_id = fields.Many2one(string='Type', comodel_name='calendar.appointment.type')
    channel = fields.Many2one(string='Channel', comodel_name='calendar.channel')
    operation_id = fields.Many2one(comodel_name="hr.operation", string="Operation")
    office_id = fields.Many2one(comodel_name="hr.department", related="operation_id.department_id", string="Office", readonly=True)
    user_id = fields.Many2one(comodel_name='res.users', string="Case worker")
    weekday = fields.Char(string='Weekday', compute="_compute_weekday")

    @api.one
    def compute_duration_text(self):
        if self.duration == 0.5:
            self.duration_text = '30 minutes'
        elif self.duration == 1.0:
            self.duration_text = '1 hour'

    @api.one
    def _compute_weekday(self):
        if self.start:
            daynum2dayname = {
                0: _("Monday"),
                1: _("Tuesday"),
                2: _("Wednesday"),
                3: _("Thursday"),
                4: _("Friday"),
                5: _("Saturday"),
                6: _("Sunday"),
            }
            self.weekday = daynum2dayname[self.start.weekday()]

    @api.multi
    def af_check_access(self):
        """ Check access for certain operations.
            This covers the following operations:
            * select_suggestion_move
            * select_suggestion
        """
        allowed = False
        denied = False
        locations = self.env.user.mapped('employee_ids.office_ids.operation_ids.location_id')
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
        raise Warning(_('You are not allowed to handle these meetings.'))

    @api.multi
    def _select_suggestion(self):
        # check state of appointment
        if self.appointment_id.state in ['reserved', 'confirmed']:
            raise Warning(_("This appointment is already booked."))

        occasions = self.env['calendar.occasion']
        for occasion in self.occasion_ids:
            # Ensure that occasions are still free
            if not occasion.appointment_id:
                occasions |= occasion
            else:
                free_occasion = occasion.search(
                    [
                        ('start', '=', self.start),
                        ('type_id', '=', self.type_id.id),
                        ('appointment_id', '=', False)
                    ], limit=1)
                if not free_occasion:
                    raise Warning(
                        _("No free occasions. This shouldn't happen. Please contact the system administrator."))

                occasions |= free_occasion

        app_vals = {}

        if self.channel == self.env.ref('calendar_channel.channel_local'):
            app_vals['user_id'] = occasions[0].user_id.id

        app_vals['state'] = 'confirmed'
        app_vals['start'] = self.start
        app_vals['stop'] = self.stop

        # Write data to appointment_id
        occasions.write({'appointment_id': self.appointment_id.id})
        self.appointment_id.write(app_vals)
    
    @api.multi
    def select_suggestion_move(self):
        # Perform access control.
        if self.af_check_access():
            # Checks passed. Run inner function with sudo.
            return self.sudo()._select_suggestion_move()
        raise Warning(_('You are not allowed to handle these meetings.'))

    @api.multi
    def _select_suggestion_move(self):
        occasions = self.env['calendar.occasion']
        for occasion in self.occasion_ids:
            # Ensure that occasions are still free
            if not occasion.appointment_id:
                occasions |= occasion
            else:
                free_occasion = occasion.search(
                    [
                        ('start', '=', self.start),
                        ('type_id', '=', self.type_id.id),
                        ('appointment_id', '=', False)
                    ], limit=1)
                if not free_occasion:
                    raise Warning(
                        _("No free occasions. This shouldn't happen. Please contact the system administrator."))

                occasions |= free_occasion
        self.appointment_id.move_appointment(occasions, self.appointment_id.cancel_reason)


class CalendarAppointment(models.Model):
    _name = 'calendar.appointment'
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

    name = fields.Char(string='Name', required=True)
    start = fields.Datetime(string='Start', required=True, help="Start date of an appointment",
                            default=lambda self: datetime.now())
    stop = fields.Datetime(string='Stop', required=True, help="Stop date of an appointment")
    duration_selection = fields.Selection(string="Duration",
                                          selection=[('30 minutes', '30 minutes'), ('1 hour', '1 hour')])
    duration_text = fields.Char(string="Duration", compute="compute_duration_text")
    duration = fields.Float('Duration')
    user_id = fields.Many2one(string='Case worker', comodel_name='res.users', help="Booked case worker")
    user_id_local = fields.Many2one(string='Case worker', comodel_name='res.users', help="Booked case worker",
                                    domain=_local_user_domain)
    partner_id = fields.Many2one(string='Customer', comodel_name='res.partner', help="Booked customer",
                                 default=lambda self: self.default_partners())
    state = fields.Selection(selection=[('free', 'Draft'),
                                        ('reserved', 'Reserved'),
                                        ('confirmed', 'Confirmed'),
                                        ('done', 'Done'),
                                        ('canceled', 'Canceled')],
                                        string='State', 
                                        default='free', 
                                        help="Status of the meeting")
    cancel_reason = fields.Many2one(string='Cancel reason', comodel_name='calendar.appointment.cancel_reason', help="Cancellation reason")
    cancel_reason_temp = fields.Many2one(string='Cancel reason', comodel_name='calendar.appointment.cancel_reason', store=False, help="Cancellation reason")
    operation_id = fields.Many2one(string='Operation', comodel_name='hr.operation')
    office_id = fields.Many2one(comodel_name='hr.department', string="Office", related="operation_id.department_id", readonly=True)
    occasion_ids = fields.One2many(comodel_name='calendar.occasion', inverse_name='appointment_id', string="Occasion")
    type_id = fields.Many2one(string='Type', required=True, comodel_name='calendar.appointment.type')
    channel = fields.Many2one(string='Channel', required=True, comodel_name='calendar.channel',
                              related='type_id.channel', readonly=True)
    channel_name = fields.Char(string='Channel', related='type_id.channel.name', readonly=True)
    additional_booking = fields.Boolean(String='Over booking', related='occasion_ids.additional_booking')
    reserved = fields.Datetime(string='Reserved', help="Occasions was reserved at this date and time")
    description = fields.Text(string='Description')
    suggestion_ids = fields.One2many(comodel_name='calendar.appointment.suggestion', inverse_name='appointment_id',
                                     string='Suggested Dates')
    case_worker_name = fields.Char(string="Case worker", compute="compute_case_worker_name")
    active = fields.Boolean(string='Active', default=True)
    show_suggestion_ids = fields.Boolean(string="Show suggestions", default=False)
    weekday = fields.Char(string="Weekday", compute="_compute_weekday")
    start_time = fields.Char(string='Appointment start time', readonly=True, compute='_app_start_time_calc', store=True)

    @api.one
    def compute_duration_text(self):
        if self.duration == 0.5:
            self.duration_text = '30 minutes'
        elif self.duration == 1.0:
            self.duration_text = '1 hour'

    @api.depends('start')
    def _app_start_time_calc(self):
        offset = int(self[0].start.astimezone(pytz.timezone(LOCAL_TZ)).utcoffset().total_seconds() / 60 / 60)
        for app in self:
            app.start_time = "%s:%s" % (str(app.start.hour + offset).rjust(2, '0'), str(app.start.minute).ljust(2, '0'))

    @api.one
    def _compute_weekday(self):
        if self.start:
            daynum2dayname = {
                0: _("Monday"),
                1: _("Tuesday"),
                2: _("Wednesday"),
                3: _("Thursday"),
                4: _("Friday"),
                5: _("Saturday"),
                6: _("Sunday"),
            }
            self.weekday = daynum2dayname[self.start.weekday()]

    @api.one
    def compute_case_worker_name(self):
        if self.channel == self.env.ref('calendar_channel.channel_pdm'):
            self.case_worker_name = _("Employment service officer")
        else:
            self.case_worker_name = self.user_id.login

    @api.model
    def default_partners(self):
        """ When active_model is res.partner, the current partners should be attendees """
        partners = self.env['res.partner']
        active_id = self._context.get('active_id')
        if self._context.get('active_model') == 'res.partner' and active_id:
            if active_id not in partners.ids:
                partners |= self.env['res.partner'].browse(active_id)
        return partners

    @api.onchange('type_id', 'partner_id')
    def check_partner_match_area(self):
        if self.type_id and not self.partner_id.match_area and 'KROM' in self.type_id.name:
            self.type_id = False
            raise Warning('Jobseeker not KROM classified')

    @api.onchange('type_id')
    def set_duration_selection(self):
        self.name = self.type_id.name
        if self.duration == 0.5:
            self.duration_selection = '30 minutes'
        elif self.duration == 1.0:
            self.duration_selection = '1 hour'

    # Accurate Duration based on Selected Type
    @api.onchange('type_id')
    def set_duration_type(self):
        if self.type_id:
            if self.type_id.duration_30 is True:
                self.duration_selection = '30 minutes'
            elif self.type_id.duration_60:
                self.duration_selection = '1 hour'
            else:
                self.duration_selection = False
        else:
            self.duration_selection = False

    @api.onchange('duration_selection')
    def set_duration(self):
        if self.duration_selection == "30 minutes":
            self.duration = 0.5
        if self.duration_selection == "1 hour":
            self.duration = 1.0

    @api.onchange('partner_id', 'user_id', 'start', 'duration', 'type_id', 'channel')
    def hide_suggestion_ids(self):
        self.show_suggestion_ids = False

    @api.multi
    def af_check_access(self):
        """ Check access for certain operations that require sudo.
            This covers the following operations:
            * compute_suggestion_ids
        """
        allowed = False
        denied = False
        locations = self.env.user.mapped('employee_ids.office_ids.operation_ids.location_id')
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
        if not self.env.user.has_group('af_security.af_meeting_planner'):
            return False
        local_channel = self.env.ref('calendar_channel.channel_local')
        for appointment in self:
            # ensure that appointment is local
            if appointment.channel != local_channel:
                return False
            # ensure that user has access to the appointment location.
            if appointment.mapped('operation_id.location_id') not in locations:
                return False
        return True
    
    @api.multi
    def check_access_jobseeker_officer(self):
        """Check if the user has access to this jobseeker."""
        try:
            # Ensure jobseeker access
            for appointment in self:
                if appointment.partner_id.jobseeker_access not in ('STARK', 'MYCKET_STARK'):
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
        raise Warning(_('You are not allowed to handle these meetings.'))

    @api.one
    def _compute_suggestion_ids(self):
        if not all((self.duration, self.type_id, self.channel)):
            return
        if self.channel != self.env.ref('calendar_channel.channel_pdm') and not self.operation_id:
            return
        # checking if we allow meetings of this length
        allowed_durations = []
        if self.type_id.duration_60:
            allowed_durations += [1]
        if self.type_id.duration_30:
            allowed_durations += [0.5]
        if self.duration not in allowed_durations:
            raise Warning(_("This duration is not allowed for the meeting type."))
        
        start = self.start_meeting_search(self.type_id)
        stop = self.stop_meeting_search(start, self.type_id)
        self.show_suggestion_ids = True
        suggestion_ids = []
        if self.suggestion_ids:
            suggestion_ids.append((5,))
        occasions = self.env['calendar.occasion'].get_bookable_occasions(start, stop, self.duration * 60, self.type_id, self.operation_id, max_depth = 1)
        for day in occasions:
            for day_occasions in day:
                for occasion in day_occasions:
                    suggestion_ids.append((0, 0, {
                        # Add occasions-data on suggestions
                        'start': occasion[0].start,
                        'stop': occasion[-1].stop,
                        'duration': len(occasion) * 30,
                        'type_id': occasion[0].type_id.id,
                        'channel': occasion[0].channel.id,
                        'operation_id': occasion[0].operation_id.id,
                        'user_id': occasion[0].user_id,
                        'occasion_ids': [(6, 0, occasion._ids)],
                    }))
        self.suggestion_ids = suggestion_ids

    @api.onchange('duration', 'start')
    def onchange_duration_start(self):
        if self.start and self.duration:
            self.stop = self.start + timedelta(minutes=int(self.duration * 60))

    @api.onchange('channel')
    def onchange_channel(self):
        if self.type_id and (self.channel != self.type_id.channel):
            self.type_id = False
            self.operation_id = False

    @api.onchange('channel_name')
    def onchange_channel_name(self):
        channel = self.env['calendar.channel'].search([('name', '=', self.name)])
        if channel:
            self.channel = channel.id

    @api.onchange('user_id_local')
    def onchange_user_id_local(self):
        if self.user_id_local:
            # TODO: add check and transfer occasions
            free_occ = self.env['calendar.occasion'].search(
                [('id', 'in', self.user_id.free_occ), ('start', '=', self.start)])
            if free_occ:
                self.occasion_ids = [(6, 0, free_occ._ids)]
                self.user_id = self.user_id_local
            else:
                raise Warning(_("Case worker has no free occasions at that time."))

    def _check_resource_calendar_date(self, check_date):
        """Checks if a date is overlapping with a holiday from resource.calender.leaves """
        res = self.env['resource.calendar.leaves'].sudo().search_read(
            [('date_from', '<=', check_date), ('date_to', '>=', check_date)])
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
            if (loop_start.weekday() in [0, 1, 2, 3, 4]) and self._check_resource_calendar_date(loop_start):
                i += 1

        return loop_start.replace(hour=BASE_DAY_START.hour, minute=BASE_DAY_START.minute, second=0, microsecond=0)

    def stop_meeting_search(self, start_meeting_search, type_id):
        days_last = self.type_id.days_last if self.type_id.days_last else 15
        # remove one day from start date since we add a day at the start of each loop.
        loop_start = start_meeting_search - timedelta(days=1)
        i = 0

        while i < days_last:
            loop_start = loop_start + timedelta(days=1)
            if (loop_start.weekday() in [0, 1, 2, 3, 4]) and self._check_resource_calendar_date(loop_start):
                i += 1

        return loop_start.replace(hour=BASE_DAY_STOP.hour, minute=BASE_DAY_STOP.minute, second=0, microsecond=0)

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
        raise Warning(_('You are not allowed to cancel these meetings.'))

    def _cancel(self, cancel_reason):
        # Do not allow cancelation of meetings that have been sent to ACE
        if not cancel_reason:
            return False
        for appointment in self:
            if appointment.state == 'confirmed':
                appointment.state = 'canceled'
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
        raise Warning(_('You are not allowed to confirm these meetings.'))

    def _confirm_appointment(self):
        for appointment in self:
            if appointment.state == 'reserved':
                appointment.state = 'confirmed'

                res = True
            else:
                res = False

            return res


    @api.multi
    def write(self, vals):
        if (self.occasion_ids != False) and (self.channel == self.env.ref('calendar_channel.channel_local')) and (
                vals.get('start') or vals.get('stop') or vals.get('type_id')):
            self._check_remaining_occasions()
        if vals.get('cancel_reason_temp'):
            vals['cancel_reason'] = vals.pop('cancel_reason_temp')
        res = super(CalendarAppointment, self).write(vals)
        return res

    @api.multi
    def _check_remaining_occasions(self):
        start_check = datetime.now() + timedelta(days=self.type_id.days_first)
        stop_check = datetime.now() + timedelta(days=self.type_id.days_last)
        min_num = self.env['calendar.appointment.type.operation'].sudo().search([('operation_id', '=', self.operation_id.id), ('type_id', '=', self.type_id.id)], limit=1).warning_threshold

        if min_num:
            occ_num = self.env['calendar.occasion'].search_count([
                ('start', '>', start_check),
                ('start', '<', stop_check),
                ('type_id', '=', self.type_id.id),
                ('additional_booking', '=', False),
                ('appointment_id', '=', False),
                ('state', 'in', ['free', 'confirmed']),
                ('operation_id', '=', self.operation_id.id)])

            if occ_num < min_num:
                if self.operation_id.app_warn_emp_ids:
                    for user in self.operation_id.app_warn_emp_ids:
                        template = self.env.ref('calendar_af.email_template_low_occasion_warning')
                        template.email_to = user.work_email
                        template.send_mail(self.id, force_send=True)
                else:
                    _logger.debug(_("No threshold users setup for operation %s") % self.operation_id.name)
        else:
            _logger.debug(_("No threshold set for operation %s and meeting type %s") % (self.operation_id.name, self.type_id.name))

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
            "res_model": "calendar.appointment",
            "res_id": self._context.get("active_id", False),
            "view_type": "form",
            "view_mode": "form",
            "view_id": self.env.ref(
                "calendar_af.view_calendar_appointment_move_form"
            ).id,
            "target": "inline",
            "type": "ir.actions.act_window",
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
        """"Intended to be used to move appointments from one bookable occasion to another. 
        :param occasions: a recordset of odoo occasions to move the meeting to."""
        res = False

        if occasions:
            # replace the occasions for the appointment
            vals = {
                'start': occasions[0].start,
                'stop': occasions[-1].stop,
                'duration': len(occasions) * BASE_DURATION / 60,
                'type_id': occasions[0].type_id.id,
                'additional_booking': False,
                'occasion_ids': [(6, 0, occasions._ids)],
            }
            self.write(vals)

            self.generate_move_daily_note(occasions, reason)
            res = True

        return res

    @api.model
    def delete_reservation(self, occasions):
        """Deletes a reservation
        :param occasions: a recordset of odoo occasions linked to a reservation"""
        reservation = self.env['calendar.appointment'].sudo().search(
            [('occasion_ids', 'in', occasions._ids), ('state', '=', 'reserved')])
        if reservation:
            reservation.unlink()
            return True
        else:
            return False


class CalendarAppointmentCancelReason(models.Model):
    _name = 'calendar.appointment.cancel_reason'
    _description = "Cancellation reason for an appointment"

    name = fields.Char(string='Name', required=True, translate=True)
    appointment_id = fields.One2many(comodel_name='calendar.appointment', inverse_name='cancel_reason')


class CalendarOccasion(models.Model):
    _name = 'calendar.occasion'
    _description = "Occasion"

    name = fields.Char(string='Name', required=True)
    start = fields.Datetime(string='Start', required=True, help="Start date of an occasion", index=True)
    stop = fields.Datetime(string='Stop', required=True, help="Stop date of an occasion")
    duration_selection = fields.Selection(string="Duration",
                                          selection=[('30 minutes', '30 minutes'), ('1 hour', '1 hour')])
    duration = fields.Float('Duration')
    duration_text = fields.Char('Duration', compute="compute_duration_text", store=True)
    appointment_id = fields.Many2one(comodel_name='calendar.appointment', string="Appointment", index=True)
    type_id = fields.Many2one(comodel_name='calendar.appointment.type', string='Type', index=True)
    channel = fields.Many2one(string='Channel', comodel_name='calendar.channel', related='type_id.channel',
                              readonly=True)
    channel_name = fields.Char(string='Channel', related='type_id.channel.name', readonly=True)
    additional_booking = fields.Boolean(String='Over booking', index=True)
    user_id = fields.Many2one(string='Case worker', comodel_name='res.users', help="Booked case worker", index=True)
    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('request', 'Published'),
                                        ('ok', 'Accepted'),
                                        ('fail', 'Rejected'),
                                        ('booked', 'Booked'),
                                        ('deleted', 'Deleted')],
                                        string='Occasion state', 
                                        default='request', 
                                        help="Status of the meeting", index=True)
    operation_id = fields.Many2one(comodel_name='hr.operation', string="Operation", index=True)
    office_id = fields.Many2one(comodel_name='hr.department', string="Office", related="operation_id.department_id", readonly=True)
    start_time = fields.Char(string='Occasion start time', readonly=True, compute='_occ_start_time_calc', store=True)
    weekday = fields.Char(string='Weekday', compute="_compute_weekday")
    is_possible_start = fields.Selection(string='Is a possible start time', 
                                         selection=[('', 'Not set'),
                                                    ('0', 'No'),
                                                    ('1', 'Yes')])
    occasion_ids = fields.Many2many(
        comodel_name="calendar.occasion",
        relation="calendar_occasion_related",
        column1="occasion_1",
        column2="occasion_2",
        string="Related occasions",
        readonly=True,
    )

    @api.one
    def compute_duration_text(self):
        self.duration_text = "%s minutes" % int(self.duration)

    @api.one
    def _compute_weekday(self):
        if self.start:
            daynum2dayname = {
                0: _("Monday"),
                1: _("Tuesday"),
                2: _("Wednesday"),
                3: _("Thursday"),
                4: _("Friday"),
                5: _("Saturday"),
                6: _("Sunday"),
            }
            self.weekday = daynum2dayname[self.start.weekday()]

    @api.depends('start')
    def _occ_start_time_calc(self):
        offset = int(self[0].start.astimezone(pytz.timezone(LOCAL_TZ)).utcoffset().total_seconds() / 60 / 60)
        for occ in self:
            occ.start_time = "%s:%s" % (str(occ.start.hour + offset).rjust(2, '0'), str(occ.start.minute).ljust(2, '0'))

    @api.onchange('type_id')
    def set_duration_selection(self):
        self.name = self.type_id.name
        if self.duration == 0.5:
            self.duration_selection = '30 minutes'
        elif self.duration == 1.0:
            self.duration_selection = '1 hour'

    @api.onchange('duration_selection')
    def set_duration(self):
        if self.duration_selection == "30 minutes":
            self.duration = 0.5
        if self.duration_selection == "1 hour":
            self.duration = 1.0
        self.onchange_duration_start()

    @api.onchange('duration', 'start')
    def onchange_duration_start(self):
        if self.start and self.duration:
            self.stop = self.start + timedelta(minutes=int(self.duration * 60))

    @api.model
    def _force_create_occasion(self, duration, start, type_id, channel, state, user=False, operation_id=False, additional_booking=True):
        """In case we need to force through a new occasion for some reason"""
        vals = {
            'name': _('%sm @ %s') % (duration, pytz.timezone(LOCAL_TZ).localize(start)),
            'start': start,
            'stop': start + timedelta(minutes=duration),
            'duration': duration,
            'appointment_id': False,
            'type_id': type_id,
            'channel': channel,
            'operation_id': operation_id.id if operation_id else False,
            'user_id': user.id if user else False,
            'additional_booking': additional_booking,
            'state': state,
        }
        res = self.env['calendar.occasion'].create(vals)
        return res

    @api.model
    def _get_min_occasions(self, type_id, date_start=None, date_stop=None):
        """Returns the timeslot (as a start date, DateTime) with the least 
        amount of occurances for a specific timeframe"""
        date_start = date_start or copy.copy(BASE_DAY_START)
        # Additional occasions should not be created after 15:00
        date_stop = date_stop or copy.copy(BASE_DAY_STOP)
        loop_date = date_start
        occ_time = {}
        while loop_date < date_stop:
            # do not check saturday or sunday
            # if loop_date.weekday() not in [5,6]:
            # make sure we don't book meetings during lunch (11:00-12:00)
            if (loop_date.hour != BASE_DAY_LUNCH.hour) and not (
                type_id.duration == 60
                and 
                (
                    (
                        loop_date.hour == BASE_DAY_LUNCH.hour - 1
                        and loop_date.minute == 30
                    ) 
                    or 
                    (
                        loop_date.hour == date_stop.hour - 1 
                        and loop_date.minute == 30
                    )
                )
            ):
                occ_time[loop_date.strftime("%Y-%m-%dT%H:%M:%S")] = self.env['calendar.occasion'].search_count(
                    [('start', '=', loop_date), ('type_id', '=', type_id.id)])
            loop_date = loop_date + timedelta(minutes=BASE_DURATION)
        occ_time_min_key = min(occ_time, key=occ_time.get)
        res = datetime.strptime(occ_time_min_key, "%Y-%m-%dT%H:%M:%S")
        return res

    @api.model
    def _check_date_mapping(self, date, operation_id=False):
        """Checks if a date has a mapped date, and returns the mapped date 
        if it exists """
        if operation_id:
            mapped_date = self.env['calendar.mapped_dates'].search([('from_date', '=', date), ('operation_id', '=', operation_id.id)])
        else:
            mapped_date = self.env['calendar.mapped_dates'].search([('from_date', '=', date), ('operation_id', '=', False)])
        if mapped_date:
            res = mapped_date.to_date
        else:
            res = date
        return res

    @api.model
    def _get_additional_booking(self, date, duration, type_id, operation_id=False):
        """"Creates extra, additional, occasions. Iff overbooking is allowed. """
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
        day_start = copy.copy(BASE_DAY_START)
        day_stop = copy.copy(BASE_DAY_STOP) - timedelta(hours=1)
        # Ugly, ugly code..
        day_start = day_start.replace(year=int(date_list[0]), month=int(date_list[1]), day=int(date_list[2]))
        day_stop = day_stop.replace(year=int(date_list[0]), month=int(date_list[1]), day=int(date_list[2]))
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
        else:
            start_date = self._get_min_occasions(type_id, day_start, day_stop)
        # Calculate how many occasions we need
        no_occasions = int(duration / BASE_DURATION)
        if operation_id:
            if operation_id.reserve_admin_ids:
                # find employees listed as available for reserve bookings on operation
                employee_ids = operation_id.reserve_admin_ids
                # select random employee from the recordset
                user_id = employee_ids[randint(0,len(employee_ids)-1)].user_id
            else:
                # no user_id could be set.
                raise Warning(_("No case worker could be set for operation %s") % operation_id.operation_code)

        # Create new occasions.
        res = self.env['calendar.occasion']
        for i in range(no_occasions):
            vals = {
                'name': '%sm @ %s' % (duration, start_date),
                'start': start_date,
                'stop': start_date + timedelta(minutes=BASE_DURATION),
                'duration': BASE_DURATION / 60,
                'appointment_id': False,
                'type_id': type_id.id,
                'channel': type_id.channel.id,
                'operation_id': operation_id.id if operation_id else False,
                'user_id': user_id.id if user_id else False, 
                'additional_booking': True,
                'state': 'ok',
            }
            res |= self.env['calendar.occasion'].create(vals)
            start_date = start_date + timedelta(minutes=BASE_DURATION)
        return res

    @api.multi
    def check_access_planner_locations(self, locations):
        """Check if current user is planner with access to these locations."""
        if not self.env.user.has_group('af_security.af_meeting_planner'):
            return False
        for occasion in self:
            # ensure that user has access to at least one location per occasion.
            if not occasion.mapped('office_id.operation_ids.location_id') & locations:
                return False
        return True

    @api.multi
    def af_check_access(self):
        """ Perform access control before allowing certain operations.
            Controls access for:
            * publish_occasion
            * accept_occasion
            * reject_occasion
            * delete_occasion
        """
        allowed = False
        denied = False
        locations = self.env.user.mapped('employee_ids.office_ids.operation_ids.location_id')
        # Check access for Meeting Planner
        if self.check_access_planner_locations(locations):
            allowed = True
        if allowed and not denied:
            return True
        return False
    
    @api.multi
    def publish_occasion(self):
        """User publishes suggested occasion"""
        # Perform access control.
        if self.af_check_access():
            # Checks passed. Run inner function with sudo.
            return self.sudo()._publish_occasion()
        raise Warning(_('You are not allowed to publish these occasions.'))

    @api.multi
    def _publish_occasion(self):
        if self.state == 'draft' or self.state == 'fail':
            self.state = 'request'
            for occasion_id in self.occasion_ids:
                occasion_id.state = 'request'
            ret = True
        else:
            ret = False

        return ret

    @api.multi
    def accept_occasion(self):
        """User accepts suggested occasion"""
        # Perform access control.
        if self.af_check_access():
            # Checks passed. Run inner function with sudo.
            return self.sudo()._accept_occasion()
        raise Warning(_('You are not allowed to accept these occasions.'))
    
    def _accept_occasion(self):
        if self.state == 'request' or self.state == 'fail':
            self.state = 'ok'
            for occasion_id in self.occasion_ids:
                occasion_id.state = 'ok'
            ret = True
        else:
            ret = False

        return ret

    @api.multi
    def reject_occasion(self):
        """User rejects suggested occasion"""
        # Perform access control.
        if self.af_check_access():
            # Checks passed. Run inner function with sudo.
            return self.sudo()._reject_occasion()
        raise Warning(_('You are not allowed to accept these occasions.'))

    @api.multi
    def _reject_occasion(self):
        if self.state in ['request', 'ok'] and not self.appointment_id:
            self.state = 'fail'
            for occasion_id in self.occasion_ids:
                occasion_id.state = 'fail'
            ret = True
        else:
            ret = False

        return ret

    @api.multi
    def delete_occasion(self):
        """User deletes an occasion"""
        # Perform access control.
        if self.af_check_access():
            # Checks passed. Run inner function with sudo.
            return self.sudo()._delete_occasion()
        raise Warning(_('You are not allowed to delete these occasions.'))

    @api.multi
    def _delete_occasion(self):
        if not self.appointment_id:
            self.state = 'deleted'
            ret = True
        else:
            ret = False

        return ret

    @api.model
    def get_bookable_occasions(self, start, stop, duration, type_id, operation_id=False, max_depth=1):
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
        no_occasions = int(duration / BASE_DURATION)
        date_delta = (stop - start)
        td_base_duration = timedelta(minutes=BASE_DURATION)

        occ_lists = []
        # declare lists for each day
        for i in range(date_delta.days + 1):
            occ_lists.append([])

        sql_type_id = type_id.id
        sql_start = start
        sql_stop = stop
        sql_max_depth = max_depth

        # do search for local offices
        if type_id.channel == self.env.ref('calendar_channel.channel_local') and operation_id:
            # Specific variables for local offices
            sql_operation_id = operation_id.id
            sql_occasion_ids = "AND cor.occasion_1 IS NULL AND cor.occasion_2 IS NULL" if no_occasions == 1 else ""

            sql_query = f"""SELECT user_id, start::date as start_date, start::time as start_time, array_agg(DISTINCT(id))
                            FROM calendar_occasion co
                                LEFT JOIN calendar_occasion_related cor
                                    ON cor.occasion_1 = co.id
                                        OR cor.occasion_2 = co.id
                            WHERE appointment_id IS NULL 
                                AND additional_booking = 'f'
                                {sql_occasion_ids}
                                AND type_id = {sql_type_id}
                                AND start >= '{sql_start}'
                                AND start <= '{sql_stop}'
                                AND operation_id = {sql_operation_id}
                                AND state = 'ok'
                            GROUP BY start::time, start::date, user_id
                            ORDER BY user_id ASC, start_date DESC, start_time ASC;"""
            self._cr.execute(sql_query)
            sql_res = self._cr.fetchall()

            # handle 30 min meetings
            if type_id.duration == 30:
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
                        day_num =+ 1
                    occasions = []
                    if len(occ_lists[day_num]) < max_depth:
                        for i in range(min(max_depth, len(curr_starts))):
                            occ_id = self.env['calendar.occasion'].browse(curr_starts[i])
                            occasions.append(occ_id)
                    occ_lists[day_num].append(occasions)
                    prev_date = curr_date
                    prev_user_id = curr_user_id
            # hardcoded for 60 min meetings for now...
            else:
                count_prev_starts = 0
                prev_starts = []
                prev_user_id = False
                prev_date = False
                day_num = 0
                # find occasions for each slot, starting with last day
                for dt_occ_pair in sql_res:
                    curr_user_id = dt_occ_pair[0]
                    curr_date = dt_occ_pair[1]
                    curr_starts = dt_occ_pair[3]
                    if not prev_date:
                        # for the first iteration, set variables and skip
                        prev_date = curr_date
                        prev_starts = curr_starts
                        prev_user_id = curr_user_id
                        count_prev_starts = 0
                        # skip first iteration
                        continue
                    if curr_user_id != prev_user_id:
                        day_num = 0
                        count_prev_starts = 0
                        prev_starts = curr_starts
                        prev_date = curr_date
                        prev_user_id = curr_user_id
                        # skip first iteration for each user
                        continue
                    if curr_date != prev_date:
                        # new day, reset count_prev_starts.
                        count_prev_starts = 0
                        day_num =+ 1
                    else:
                        count_prev_starts = max(len(curr_starts)-count_prev_starts,0)
                    limit = min(count_prev_starts, max_depth)
                    if limit != 0:
                        occasions = []
                        for i in range(limit):
                            first_occ = self.env['calendar.occasion'].browse(prev_starts[i])
                            second_occ = self.env['calendar.occasion'].browse(curr_starts[i])
                            first_occ |= second_occ
                            occasions.append(first_occ)
                        occ_lists[day_num].append(occasions)
                    prev_date = curr_date
                    prev_starts = curr_starts
                    prev_user_id = curr_user_id
        # Do PDM search
        else:
            sql_query = f"""SELECT start::date as start_date, start::time as start_time, array_agg(id)
                            FROM calendar_occasion
                            WHERE appointment_id IS NULL
                                AND additional_booking = 'f' 
                                AND type_id = {sql_type_id}
                                AND start >= '{sql_start}'
                                AND start <= '{sql_stop}'
                                AND state = 'ok'
                            GROUP BY start::time, start::date
                            ORDER BY start_date DESC, start_time ASC;"""
            self._cr.execute(sql_query)
            sql_res = self._cr.fetchall()

            # handle 30 min meetings
            if type_id.duration == 30:
                prev_date = False
                day_num = 0
                for dt_occ_pair in sql_res:
                    curr_date = dt_occ_pair[0]
                    curr_starts = dt_occ_pair[2]
                    if not prev_date:
                        prev_date = curr_date
                    if curr_date != prev_date:
                        day_num =+ 1
                    occasions = []
                    for i in range(min(max_depth, len(curr_starts))):
                        occ_id = self.env['calendar.occasion'].browse(curr_starts[i])
                        occasions.append(occ_id)
                    occ_lists[day_num].append(occasions)
                    prev_date = curr_date
            # hardcoded for 60 min meetings for now...
            else:
                count_prev_starts = 0
                prev_starts = []
                prev_date = False
                day_num = 0
                # find occasions for each slot, starting with last day
                for dt_occ_pair in sql_res:
                    curr_date = dt_occ_pair[0]
                    curr_starts = dt_occ_pair[2]
                    if not prev_date:
                        # for the first iteration, set variables and skip
                        prev_date = curr_date
                        prev_starts = curr_starts
                        count_prev_starts = 0
                        continue
                    if curr_date != prev_date:
                        # new day, reset count_prev_starts.
                        count_prev_starts = 0
                        day_num =+ 1
                    else:
                        count_prev_starts = max(len(curr_starts)-count_prev_starts,0)
                    limit = min(count_prev_starts, max_depth)
                    if limit != 0:
                        occasions = []
                        for i in range(limit):
                            first_occ = self.env['calendar.occasion'].browse(prev_starts[i])
                            second_occ = self.env['calendar.occasion'].browse(curr_starts[i])
                            first_occ |= second_occ
                            occasions.append(first_occ)
                        occ_lists[day_num].append(occasions)
                    prev_date = curr_date
                    prev_starts = curr_starts

        # if type allows additional bookings and we didn't find any
        # free occasions, create new ones:
        if type_id.additional_booking and all(not l for l in occ_lists):
            # Changed this line to create over bookings on the LAST allowed date.
            occ_lists[-1].append([self._get_additional_booking(stop, duration, type_id, operation_id)])

        return occ_lists

    @api.model
    def reserve_occasion(self, occasion_ids):
        """Reserves an occasion."""
        start = occasion_ids[0].start
        stop = occasion_ids[len(occasion_ids) - 1].stop
        duration = (stop - start).seconds/60/60
        # type_id = self.env.ref('calendar_meeting_type.type_00').id
        type_id = occasion_ids[0].type_id

        # check that occasions are free and unreserved
        free = True
        for occasion_id in occasion_ids:
            if (occasion_id.appointment_id and occasion_id.appointment_id.state != 'reserved') or (
                    occasion_id.appointment_id and occasion_id.appointment_id.state == 'reserved' and occasion_id.appointment_id.reserved > datetime.now() - timedelta(
                seconds=RESERVED_TIMEOUT)):
                free = False

        if free:
            vals = {
                'name': type_id.name,
                'start': start,
                'stop': stop,
                'duration': duration,
                'type_id': type_id.id,
                'user_id': False,
                'partner_id': False,
                'state': 'reserved',
                'operation_id': False,
                'occasion_ids': occasion_ids, # I dont think this does anything?
                'reserved': datetime.now(),
            }
            appointment = self.env['calendar.appointment'].create(vals)

            # relation needs to be set from calendar.occasion?
            for occasion_id in occasion_ids:
                occasion_id.appointment_id = appointment.id

            res = appointment
        else:
            res = False

        return res

    @api.model
    def autovacuum_additional_occasion(self):
        del_occ = self.env['calendar.occasion'].sudo().search(
            [('additional_booking', '=', True), ('appointment_id', '=', False)])
        _logger.debug("Removing the following additional occasions: %s" % del_occ)
        del_occ.unlink()
