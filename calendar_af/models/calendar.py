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

from odoo import models, fields, api, _
from datetime import datetime, timedelta, date
from odoo.exceptions import Warning
import pytz
import copy
import logging

_logger = logging.getLogger(__name__)

# TODO: decide if we are dependent on this variable or the imported schedule duration.
# LOCAL_TZ: Local timezone 
LOCAL_TZ = 'Europe/Stockholm'
# BASE_DURATION: Base duration given by TeleOpti. This is the duration of the calendar.schedule slots in minutes.
BASE_DURATION = 30.0
# BASE_DAY_START, BASE_DAY_STOP: The hours between which we normally accept appointments
BASE_DAY_START = pytz.timezone(LOCAL_TZ).localize(datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)).astimezone(pytz.utc)
BASE_DAY_STOP = pytz.timezone(LOCAL_TZ).localize(datetime.now().replace(hour=16, minute=0, second=0, microsecond=0)).astimezone(pytz.utc)
BASE_DAY_LUNCH = pytz.timezone(LOCAL_TZ).localize(datetime.now().replace(hour=11, minute=0, second=0, microsecond=0)).astimezone(pytz.utc)
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
    type_id = fields.Many2one(string='Meeting type', comodel_name='calendar.appointment.type', help="Related meeting type")
    channel = fields.Many2one(string='Channel', comodel_name='calendar.channel')
    active = fields.Boolean(string='Active', default=True)

    @api.one
    def inactivate(self, b = True):
        """Inactivates self. Used as a workaround to inactivate from server actions."""
        if b:
            self.active = False
        else:
            self.active = True
        return self.active

    @api.multi
    def create_occasions(self):
        """Creates a number of occasions from schedules, depending on number of scheduled agents"""
        for schedule in self:
            no_occasions = self.env['calendar.occasion'].search_count([('start', '=', schedule.start), ('type_id', '=', schedule.type_id.id), ('additional_booking', '=', False)])
            if (schedule.scheduled_agents - no_occasions) > 0:
                vals = {
                    'name': _('%sm @ %s') % (schedule.duration, pytz.timezone(LOCAL_TZ).localize(schedule.start)),
                    'duration': schedule.duration,
                    'start': schedule.start,
                    'stop': schedule.stop,
                    'type_id': schedule.type_id.id,
                    'channel': schedule.channel,
                    'additional_booking': False,
                    'state': 'ok',
                }
                for occasion in range(schedule.scheduled_agents - no_occasions):
                    self.env['calendar.occasion'].create(vals)

            elif (schedule.scheduled_agents - no_occasions) < 0:
                # TODO: handle this case better
                pass

    @api.model
    def cron_get_schedules(self, type_ids, days):

        _logger.debug("Starting cron_get_schedules for meeting types: %s at %s" % (type_ids, datetime.now()))
        route = self.env.ref('edi_af_appointment.schedule')
        cal_schedule_ids = self.env['calendar.schedule']

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
                loop_times = days/30
                while i < loop_times:
                    # handle last loop different
                    if i == loop_times:
                        cal_schedule_ids |= _create_message(start + timedelta(days=(30 * i)), start + timedelta(days=days))
                    else:
                        cal_schedule_ids |= _create_message(start + timedelta(days=(30 * i)), start + timedelta(days=(30 * (i+1))))
                    
                    i += 1

        route.run()
        cal_schedule_ids.inactivate()    
        _logger.debug("Completed cron_get_schedules for meeting types: %s at %s" % (type_ids, datetime.now()))    
        
class CalendarAppointmentType(models.Model):
    _name = 'calendar.appointment.type'
    _description = "Meeting type"
    _order = 'ipf_num'

    name = fields.Char('Meeting type name', required=True)
    ipf_id = fields.Char('Teleopti competence id', required=True, help="The IPF type id, if this is wrong the integration won't work")
    ipf_name = fields.Char('Teleopti competence name')
    channel = fields.Many2one(string='Channel', comodel_name='calendar.channel')
    duration = fields.Float(string='Duration')
    duration_default = fields.Boolean(string='Use default')
    days_first = fields.Integer(string='First allowed day for type')
    days_last = fields.Integer(string='Last allowed day for type')
    ipf_num = fields.Integer(string='Meeting type id')
    additional_booking = fields.Boolean(string='Over booking')
    text = fields.Text(string='Comment')
    skill_ids = fields.Many2many(comodel_name='hr.skill', string='Skills')

class CalendarChannel(models.Model):
    _name = 'calendar.channel'
    _description = "Channel"

    name = fields.Char('Name', required=True)

class CalendarMappedDates(models.Model):
    _name = 'calendar.mapped_dates'
    _description = "Mapped dates"

    name = fields.Char(string="Name")
    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    office_id = fields.Many2one(comodel_name='hr.department', string='Office')

class CalendarAppointmentSuggestion(models.Model):
    _name = 'calendar.appointment.suggestion'
    _description = "Bookable Occasion"

    appointment_id = fields.Many2one(comodel_name='calendar.appointment', ondelete='cascade')
    start = fields.Datetime()
    stop = fields.Datetime()
    duration = fields.Float(string='Duration') 
    occasion_ids = fields.Many2many(comodel_name='calendar.occasion', string="Occasions")
    type_id = fields.Many2one(string='Type', comodel_name='calendar.appointment.type')
    channel = fields.Many2one(string='Channel', comodel_name='calendar.channel')
    office_id = fields.Many2one(comodel_name='hr.department', string="Office")
    user_id = fields.Many2one(comodel_name='res.users', string="Case worker")
    weekday = fields.Char(string='Weekday', compute="_compute_weekday")

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
    def select_suggestion(self):
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
                    raise Warning(_("No free occasions. This shouldn't happen. Please contact the system administrator."))

                occasions |= free_occasion

        # Write data to appointment_id
        occasions.write({'appointment_id': self.appointment_id.id})
        self.appointment_id.write({
            'state': 'confirmed',
            'start': self.start,
            'stop': self.stop,
        })

    @api.multi
    def select_suggestion_move(self):
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
                    raise Warning(_("No free occasions. This shouldn't happen. Please contact the system administrator."))

                occasions |= free_occasion
        self.appointment_id.move_appointment(occasions, self.appointment_id.cancel_reason)

class CalendarAppointment(models.Model):
    _name = 'calendar.appointment'
    _description = "Appointment"

    @api.multi
    @api.depends('partner_id', 'start')
    def name_get(self):
        result = []
        for app in self:
            name = _('Meeting with %s at %s') % (app.partner_id.company_registry, app.start)
            result.append((app.id, name))
        return result

    @api.model
    def _local_user_domain(self):
        if self.partner_id:
            res = []
            res.append(('partner_id.office_id.id', '=', self.env.user.office_id.id))
            # TODO: add hr.skill check ('type_id.skills_ids', 'in', self.env.user.skill_ids)
            # TODO: add check if case worker has occasions and that these are free. Maybe use a computed field on res.users?
        else:
            res = []
        return res

    name = fields.Char(string='Name', required=True)
    start = fields.Datetime(string='Start', required=True, help="Start date of an appointment", default=lambda self: datetime.now())
    stop = fields.Datetime(string='Stop', required=True, help="Stop date of an appointment")
    duration_selection = fields.Selection(string="Duration", selection=[('30 minutes','30 minutes'), ('1 hour','1 hour')])
    duration = fields.Float('Duration')
    user_id = fields.Many2one(string='Case worker', comodel_name='res.users', help="Booked case worker")
    user_id_local = fields.Many2one(string='Case worker', comodel_name='res.users', help="Booked case worker", domain=_local_user_domain)
    partner_id = fields.Many2one(string='Customer', comodel_name='res.partner', help="Booked customer", default=lambda self: self.default_partners())
    state = fields.Selection(selection=[('free', 'Draft'),
                                        ('reserved', 'Reserved'),
                                        ('confirmed', 'Confirmed'),
                                        ('done', 'Done'),
                                        ('canceled', 'Canceled')],
                                        string='State', 
                                        default='free', 
                                        help="Status of the meeting")
    cancel_reason = fields.Many2one(string='Cancel reason', comodel_name='calendar.appointment.cancel_reason', help="Cancellation reason")
    location = fields.Char(string='Location', compute='compute_location', store=True)
    location_id = fields.Many2one(string='Location', comodel_name='hr.location', related='user_id.partner_id.location_id', readonly=True)
    office_id = fields.Many2one(comodel_name='hr.department', string="Office")
    occasion_ids = fields.One2many(comodel_name='calendar.occasion', inverse_name='appointment_id', string="Occasion")
    type_id = fields.Many2one(string='Type', required=True, comodel_name='calendar.appointment.type')
    channel =  fields.Many2one(string='Channel', required=True, comodel_name='calendar.channel', related='type_id.channel', readonly=True)
    channel_name = fields.Char(string='Channel', related='type_id.channel.name', readonly=True)
    additional_booking = fields.Boolean(String='Over booking', related='occasion_ids.additional_booking')
    reserved = fields.Datetime(string='Reserved', help="Occasions was reserved at this date and time")
    description = fields.Text(string='Description')
    suggestion_ids = fields.One2many(comodel_name='calendar.appointment.suggestion', inverse_name='appointment_id', string='Suggested Dates')
    case_worker_name = fields.Char(string="Case worker", compute="compute_case_worker_name")
    partner_pnr = fields.Char(string='Attendee SSN', related="partner_id.company_registry", readonly=True)
    active = fields.Boolean(string='Active', default=True)
    show_suggestion_ids = fields.Boolean(string="Show suggestions", default=False)
    weekday = fields.Char(string="Weekday", compute="_compute_weekday")
    start_time = fields.Char(string='Appointment start time', readonly=True, compute='_app_start_time_calc', store=True)

    @api.depends('start')
    def _app_start_time_calc(self):
        offset = int(self[0].start.astimezone(pytz.timezone(LOCAL_TZ)).utcoffset().total_seconds()/60/60)
        for app in self:
            app.start_time = "%s:%s" % (str(app.start.hour + offset).rjust(2,'0'), str(app.start.minute).ljust(2,'0'))

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

    @api.depends('user_id')
    def compute_location(self):
        for app in self:
            if app.channel_name == "PDM":
                app.location = _("Distance")
            elif app.location_id:
                app.location = app.location_id.name
            else:
                app.location = ''

    @api.one
    def compute_case_worker_name(self):
        if self.channel_name == "PDM":
            self.case_worker_name = _("Employment service officer")
        else:
            self.case_worker_name = self.user_id.login

    @api.multi
    def move_meeting_action(self):
        partner = self.env['calendar.appointment'].browse(self._context.get('active_id')).partner_id
        return {
            'name': _('Move meeting for %s - %s') % (partner.company_registry, partner.display_name),
            'res_model': 'calendar.appointment',
            'res_id': self._context.get('active_id', False),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('calendar_af.view_calendar_appointment_move_form').id,
            'target': 'current',
            'type': 'ir.actions.act_window',
        }

    @api.multi
    def cancel_meeting_action(self):
        partner = self.env['calendar.appointment'].browse(self._context.get('active_id')).partner_id
        return {
            'name': _('Cancel meeting for %s - %s') % (partner.company_registry, partner.display_name),
            'res_model': 'calendar.cancel_appointment', 
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('calendar_af.cancel_appointment_view_form').id,
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {},
        }

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

    @api.onchange('duration_selection')
    def set_duration(self):
        if self.duration_selection == "30 minutes":
            self.duration = 0.5
        if self.duration_selection == "1 hour":
            self.duration = 1.0

    @api.onchange('partner_id', 'user_id', 'start', 'duration', 'type_id', 'channel')
    def hide_suggestion_ids(self):
        self.show_suggestion_ids = False

    @api.one
    def compute_suggestion_ids(self):
        if not all((self.duration, self.type_id, self.channel)):
            return
        if self.channel_name != "PDM" and not self.office_id:
            return
        start = self.start_meeting_search(self.type_id)
        stop = self.stop_meeting_search(start, self.type_id)
        self.show_suggestion_ids = True 
        suggestion_ids = []
        if self.suggestion_ids:
            suggestion_ids.append((5,))
        occasions = self.env['calendar.occasion'].get_bookable_occasions(start, stop, self.duration * 60, self.type_id, self.office_id, max_depth = 1)
        for day in occasions:
            for day_occasions in day:
                for occasion in day_occasions:
                    suggestion_ids.append((0, 0, {
                        # Fyll i occasions-data på förslagen
                        'start': occasion[0].start,
                        'stop': occasion[-1].stop,
                        'duration': len(occasion)*30,
                        'type_id': occasion[0].type_id.id,
                        'channel': occasion[0].channel.id,
                        'office_id': occasion[0].office_id.id,
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

    @api.onchange('channel_name')
    def onchange_channel_name(self):
        channel = self.env['calendar.channel'].search([('name', '=', self.name)])
        if channel:
            self.channel = channel.id

    @api.onchange('user_id_local')
    def onchange_user_id_local(self):
        if self.user_id_local:
            # TODO: add check and transfer occasions
            free_occ = self.env['calendar.occasion'].search([('id', 'in', self.user_id.free_occ), ('start', '=', self.start)])
            if free_occ:
                self.occasion_ids = [(6, 0, free_occ._ids)]
                self.user_id = self.user_id_local
            else:
                raise Warning(_("Case worker has no free occasions at that time."))

    def _check_resource_calendar_date(self, check_date):
        """Checks if a date is overlapping with a holiday from resource.calender.leaves """
        res = self.env['resource.calendar.leaves'].sudo().search_read([('date_from', '<=', check_date), ('date_to', '>=', check_date)])
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
            if (loop_start.weekday() in [0,1,2,3,4]) and self._check_resource_calendar_date(loop_start):
                i +=1

        return loop_start.replace(hour=BASE_DAY_START.hour, minute=BASE_DAY_START.minute, second=0, microsecond=0)

    def stop_meeting_search(self, start_meeting_search, type_id):
        days_last = self.type_id.days_last if self.type_id.days_last else 15
        # remove one day from start date since we add a day at the start of each loop.
        loop_start = start_meeting_search - timedelta(days=1)
        i = 0

        while i < days_last:
            loop_start = loop_start + timedelta(days=1)
            if (loop_start.weekday() in [0,1,2,3,4]) and self._check_resource_calendar_date(loop_start):
                i +=1

        return loop_start.replace(hour=BASE_DAY_STOP.hour, minute=BASE_DAY_STOP.minute, second=0, microsecond=0)

    @api.one
    def inactivate(self, b = True):
        """Inactivates self. Used as a workaround to inactivate from server actions."""
        if b:
            self.active = False
        else:
            self.active = True
        return self.active

    def cancel(self, cancel_reason):
        """Cancels a planned meeting"""
        # Do not allow cancelation of meetings that have been sent to ACE
        if not cancel_reason:
            return False
        for appointment in self:
            if appointment.state == 'confirmed':
                appointment.state = 'canceled'
                appointment.cancel_reason = cancel_reason.id

                #create daily note
                vals = {
                    "name": _("Meeting cancelled"),
                    "partner_id": self.partner_id.id,
                    "administrative_officer": self.user_id.id,
                    "note": _("%sm meeting on %s cancelled with reason: %s") % (self.duration * 30, self.start, cancel_reason.name),
                    "note_type": self.env.ref('partner_daily_notes.note_type_as_02').id,
                    "office_id": self.partner_id.office_id.id,
                    "note_date": datetime.now(),
                }
                appointment.partner_id.sudo().notes_ids = [(0, 0, vals)]
                appointment.occasion_ids = [(5, 0, 0)]
                
                return True

    def confirm_appointment(self):
        """Confirm reserved booking"""
        for appointment in self:
            if appointment.state == 'reserved':
                appointment.state = 'confirmed'

                #create daily note
                vals = {
                    "name": _("Meeting confirmed"),
                    "partner_id": self.partner_id.id,
                    "administrative_officer": self.user_id.id,
                    "note": "%sm meeting on %s confirmed." % (self.duration * 30, self.start),
                    "note_type": self.env.ref('partner_daily_notes.note_type_as_02').id,
                    "office_id": self.partner_id.office_id.id,
                    "note_date": datetime.now(),
                }
                appointment.partner_id.notes_ids = [(0, 0, vals)]

                res = True
            else: 
                res = False

            return res

    def unlink(self):
        """Delete the record"""
        #create daily note
        vals = {
            "name": _("Meeting deleted"),
            "partner_id": self.partner_id.id,
            "administrative_officer": self.user_id.id,
            "note": _("%sm meeting on %s deleted.") % (self.duration * 30, self.start),
            "note_type": self.env.ref('partner_daily_notes.note_type_as_02').id,
            "office_id": self.partner_id.office_id.id,
            "note_date": datetime.now(),
        }
        self.partner_id.notes_ids = [(0, 0, vals)]

        res = super(CalendarAppointment, self).unlink()
        return res

    @api.model
    def create(self, values):
        res = super(CalendarAppointment, self).create(values)
        # if (res.sudo().occasion_ids != False) and (res.sudo().channel == res.env.ref('calendar_channel.channel_local')):
        #     res._check_remaining_occasions()

        if res.sudo().partner_id:
            #create daily note
            vals = {
                "name": _("Meeting created"),
                "partner_id": res.partner_id.id,
                "administrative_officer": res.user_id.id,
                "note": _("%sm meeting on %s created.") % (res.duration * 30, res.start),
                "note_type": res.env.ref('partner_daily_notes.note_type_as_02').id,
                "office_id": res.partner_id.office_id.id,
                "note_date": datetime.now(),
            }
            res.sudo().partner_id.notes_ids = [(0, 0, vals)]

        return res

    @api.multi
    def write(self, vals):
        if (self.occasion_ids != False) and (self.channel == self.env.ref('calendar_channel.channel_local')) and (vals.get('start') or vals.get('stop') or vals.get('type_id')):
            self._check_remaining_occasions()
        return super(CalendarAppointment, self).write(vals)

    @api.multi
    def _check_remaining_occasions(self):
        start_check = datetime.now() + timedelta(days=self.type_id.days_first)
        stop_check = datetime.now() + timedelta(days=self.type_id.days_last)
        min_num = self.env['calendar.appointment.type.department'].sudo().search([('office_id', '=', self.office_id.id), ('type_id', '=', self.type_id.id)], limit=1).warning_threshold

        if min_num:
            occ_num = self.env['calendar.occasion'].search_count([
                ('start', '>', start_check),
                ('start', '<', stop_check),
                ('type_id', '=', self.type_id.id),
                ('additional_booking', '=', False),
                ('appointment_id', '=', False),
                ('state', 'in', ['free', 'confirmed']),
                ('office_id', '=', self.office_id.id)])

            if occ_num < min_num:
                if self.office_id.app_warn_user_ids:
                    for user in self.office_id.app_warn_user_ids:
                        template = self.env.ref('calendar_af.email_template_low_occasion_warning')
                        template.email_to = user.work_email
                        template.send_mail(self.id, force_send=True)
                else:
                    _logger.debug(_("No threshold users setup for office %s") % self.office_id.name)
        else:
            _logger.debug(_("No threshold set for office %s and meeting type %s") % (self.office_id.name, self.type_id.name))

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
                'duration': len(occasions) * BASE_DURATION/60,
                'type_id': occasions[0].type_id.id,
                'additional_booking': False,
                'occasion_ids': [(6, 0, occasions._ids)],
            }
            self.write(vals)

            #create daily note
            vals = {
                "name": _("Meeting moved"),
                "partner_id": self.partner_id.id,
                "administrative_officer": self.user_id.id,
                "note": _("Meeting on %s moved") % self.start + (_(" because of reason: %s.") % reason.name) if reason else ".",
                "note_type": self.env.ref('partner_daily_notes.note_type_as_02').id,
                "office_id": self.partner_id.office_id.id,
            }
            self.partner_id.sudo().notes_ids = [(0, 0, vals)]
            res = True

        return res

    @api.model
    def delete_reservation(self, occasions):
        """Deletes a reservation
        :param occasions: a recordset of odoo occasions linked to a reservation"""
        reservation = self.env['calendar.appointment'].sudo().search([('occasion_ids', 'in', occasions._ids), ('state', '=', 'reserved')])
        if reservation:
            reservation.unlink()
            return True
        else:
            return False

class CalendarAppointmentCancelReason(models.Model):
    _name = 'calendar.appointment.cancel_reason'
    _description = "Cancellation reason for an appointment"

    name = fields.Char(string='Name', required=True)
    appointment_id = fields.One2many(comodel_name='calendar.appointment', inverse_name='cancel_reason')

class CalendarOccasion(models.Model):
    _name = 'calendar.occasion'
    _description = "Occasion"

    name = fields.Char(string='Name', required=True)
    start = fields.Datetime(string='Start', required=True, help="Start date of an occasion")
    stop = fields.Datetime(string='Stop', required=True, help="Stop date of an occasion")
    duration_selection = fields.Selection(string="Duration", selection=[('30 minutes','30 minutes'), ('1 hour','1 hour')])
    duration = fields.Float('Duration')
    appointment_id = fields.Many2one(comodel_name='calendar.appointment', string="Appointment")
    type_id = fields.Many2one(comodel_name='calendar.appointment.type', string='Type')
    channel = fields.Many2one(string='Channel', comodel_name='calendar.channel', related='type_id.channel', readonly=True)
    channel_name = fields.Char(string='Channel', related='type_id.channel.name', readonly=True)
    additional_booking = fields.Boolean(String='Over booking')
    user_id = fields.Many2one(string='Case worker', comodel_name='res.users', help="Booked case worker")
    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('request', 'Published'),
                                        ('ok', 'Accepted'),
                                        ('fail', 'Rejected'),
                                        ('booked', 'Booked'),
                                        ('deleted', 'Deleted')],
                                        string='Occasion state', 
                                        default='request', 
                                        help="Status of the meeting")
    office_id = fields.Many2one(comodel_name='hr.department', string="Office")
    app_partner_pnr = fields.Char(string='Attendee SSN', related="appointment_id.partner_id.company_registry", readonly=True)
    start_time = fields.Char(string='Occasion start time', readonly=True, compute='_occ_start_time_calc', store=True)
    weekday = fields.Char(string='Weekday', compute="_compute_weekday")

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
        offset = int(self[0].start.astimezone(pytz.timezone(LOCAL_TZ)).utcoffset().total_seconds()/60/60)
        for occ in self:
            occ.start_time = "%s:%s" % (str(occ.start.hour + offset).rjust(2,'0'), str(occ.start.minute).ljust(2,'0'))

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
    def _force_create_occasion(self, duration, start, type_id, channel, state, user=False, office_id=False, additional_booking=True):
        """In case we need to force through a new occasion for some reason"""
        vals = {
            'name': _('%sm @ %s') % (duration, pytz.timezone(LOCAL_TZ).localize(start)),
            'start': start,
            'stop': start + timedelta(minutes=duration),
            'duration': duration,
            'appointment_id': False,
            'type_id': type_id,
            'channel': channel,
            'office_id': office_id.id if office_id else False,
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
            # make sure we don't book meetings during lunch (11:00-12:30)
            if (loop_date.hour != BASE_DAY_LUNCH.hour) and ((loop_date.hour != BASE_DAY_LUNCH.hour + 1) and (loop_date.minute == 0)):
                occ_time[loop_date.strftime("%Y-%m-%dT%H:%M:%S")] = self.env['calendar.occasion'].search_count([('start', '=', loop_date),('type_id', '=', type_id.id)])
            loop_date = loop_date + timedelta(minutes=BASE_DURATION)
        occ_time_min_key = min(occ_time, key=occ_time.get)
        res = datetime.strptime(occ_time_min_key, "%Y-%m-%dT%H:%M:%S")
        return res

    @api.model
    def _check_date_mapping(self, date, office_id):
        """Checks if a date has a mapped date, and returns the mapped date 
        if it exists """
        mapped_date = self.env['calendar.mapped_dates'].search([('from_date', '=', date), ('office_id', '=', office_id.id)])
        if mapped_date:
            res = mapped_date.to_date 
        else:
            res = date
        return res

    @api.model
    def _get_additional_booking(self, date, duration, type_id, office_id=False):
        """"Creates extra, additional, occasions. Iff overbooking is allowed. """
        # Check if overbooking is allowed on this meeting type
        if not type_id.additional_booking:
            # TODO: Throw error instead?
            _logger.debug(_("Overbooking not allowed on %s" % type_id.name))
            return False
        # Replace date with mapped date if we have one
        date = self._check_date_mapping(date, office_id)
        date_list = date.strftime("%Y-%-m-%-d").split("-")
        # Copy to make sure we dont overwrite BASE_DAY_START or BASE_DAY_STOP
        day_start = copy.copy(BASE_DAY_START)
        day_stop = copy.copy(BASE_DAY_STOP) - timedelta(hours=1)
        # Ugly, ugly code..
        day_start = day_start.replace(year=int(date_list[0]), month=int(date_list[1]), day=int(date_list[2]))
        day_stop = day_stop.replace(year=int(date_list[0]), month=int(date_list[1]), day=int(date_list[2]))
        # Find when to create new occasion
        start_date = self._get_min_occasions(type_id, day_start, day_stop)
        # Calculate how many occasions we need
        no_occasions = int(duration / BASE_DURATION)
        # Create new occasions.
        res = self.env['calendar.occasion']
        for i in range(no_occasions):
            vals = {
                'name': '%sm @ %s' % (duration, start_date),
                'start': start_date,
                'stop': start_date + timedelta(minutes=BASE_DURATION),
                'duration': BASE_DURATION/60,
                'appointment_id': False,
                'type_id': type_id.id,
                'channel': type_id.channel.id,
                'office_id': office_id.id if office_id else False,
                'additional_booking': True,
                'state': 'ok',
            }
            res |= self.env['calendar.occasion'].create(vals)
            start_date = start_date + timedelta(minutes=BASE_DURATION)
        return res

    @api.multi
    def publish_occasion(self):
        """User publishes suggested occasion"""
        if self.state == 'draft':
            self.state = 'request'
            ret = True
        else:
            ret = False

        return ret

    @api.multi
    def accept_occasion(self):
        """User accepts suggested occasion"""
        if self.state == 'request':
            self.state = 'ok'
            ret = True
        else:
            ret = False

        return ret

    @api.multi
    def reject_occasion(self):
        """User rejects suggested occasion"""
        if self.state in ['request','ok']:
            self.state = 'fail'
            ret = True
        else:
            ret = False

        return ret

    @api.multi
    def delete_occasion(self):
        """User deletes an occasion"""
        if not self.appointment_id:
            self.state = 'deleted'
            ret = True
        else:
            ret = False

        return ret

    @api.model
    def get_bookable_occasions(self, start, stop, duration, type_id, office_id=False, max_depth=1):
        """Returns a list of occasions matching the defined parameters of the appointment. Creates additional 
        occasions if allowed.
        :param start: Start search as this time.
        :param stop: Stop search as this time.
        :param duration: Meeting length.
        :param type_id: Meeting type.
        :param max_depth: Number of bookable occasions per time slot.
        """
        # Calculate number of occasions needed to match booking duration
        no_occasions = int(duration / BASE_DURATION)
        date_delta = (stop - start)
        td_base_duration = timedelta(minutes=BASE_DURATION)
        def get_occasions(start_dt):
            start_dt = start_dt.replace(second=0, microsecond=0)
            domain = [('start', '=', start_dt), ('type_id', '=', type_id.id), ('appointment_id', '=', False), ('additional_booking', '=', False)]
            if office_id:
                domain.append(('office_id', '=', office_id.id))
            # TODO: This if can and should probably be removed but I don't want to break anything right now
            if type_id.channel == self.env.ref('calendar_channel.channel_local'):
                domain.append(('state', '=', 'ok'))
            return self.env['calendar.occasion'].search(domain, limit=max_depth)
        #[[[], []], dag[tidsslot[ocassions]]]

        occ_lists = []
        # declare lists for each day
        for i in range(date_delta.days + 1):
            occ_lists.append([])
        
        # find occasions for each day, starting with last day
        # Changes made below this line to make the code loop over dates in reverse order.
        # for day in range(date_delta.days + 1):
        for day in reversed(range(date_delta.days + 1)):
            occasions = []
            # find 'max_depth' number of free occasions for each timeslot
            if day == date_delta.days:
                start_dt = copy.copy(stop)
                start_dt = start_dt.replace(hour=BASE_DAY_START.hour, minute=BASE_DAY_START.minute)
                last_slot = copy.copy(stop)
                last_slot = last_slot.replace(hour=BASE_DAY_STOP.hour, minute=BASE_DAY_STOP.minute)
                last_slot -= timedelta(minutes=duration)
            else:
                # This will break given certain times and timezones. Should work for us.
                start_dt = start_dt - timedelta(days=1)
                start_dt = start_dt.replace(hour=BASE_DAY_START.hour, minute=BASE_DAY_START.minute)
                last_slot = last_slot - timedelta(days=1)
            while start_dt <= last_slot:
                if not occasions:
                    for i in range(no_occasions):
                        dt_start = start_dt + td_base_duration * i
                        occasions.append(get_occasions(dt_start))
                else:
                    # Remove first record in list and add a new occasion at the end
                    # This way we shift the bookable occasion 30 min forward every iteration
                    del occasions[0]
                    # The line below causes a bug that returns bookable occasions 
                    # with 30 min (1 occasion) gaps before the last 30 min (1 occasion).
                    # I fixed this with (no_occasions - 1). I have not investigated it further. 
                    occasions.append(get_occasions(start_dt + td_base_duration * (no_occasions - 1)))
                available_depth = min([len(o) for o in occasions] or [0])
                slot = []
                for i in range(available_depth):
                    slot_occasion = self.env['calendar.occasion']
                    for occ in occasions:
                        slot_occasion |= occ[i]
                    slot.append(slot_occasion)
                if slot:
                    occ_lists[day].append(slot)
                start_dt += td_base_duration

        # if type allows additional bookings and we didn't find any
        # free occasions, create new ones:
        if type_id.additional_booking and all( not l for l in occ_lists):
            # Changed this line to create over bookings on the LAST allowed date.
            occ_lists[-1].append([self._get_additional_booking(stop, duration, type_id, office_id)])

        return occ_lists

    @api.model
    def reserve_occasion(self, occasion_ids):
        """Reserves an occasion."""
        start = occasion_ids[0].start
        stop = occasion_ids[len(occasion_ids)-1].stop
        duration = stop.minute - start.minute 
        type_id = self.env.ref('calendar_meeting_type.type_00').id

        # check that occasions are free and unreserved
        free = True
        for occasion_id in occasion_ids:
            if (occasion_id.appointment_id and occasion_id.appointment_id.state != 'reserved') or (occasion_id.appointment_id and occasion_id.appointment_id.state == 'reserved' and occasion_id.appointment_id.reserved > datetime.now() - timedelta(seconds=RESERVED_TIMEOUT)):
                free = False

        if free:
            vals = {
                'name': occasion_ids[0].type_id.name,
                'start': start,
                'stop': stop,
                'duration': duration,
                'type_id': type_id,
                'user_id': False,
                'partner_id': False,
                'state': 'reserved',
                'office_id': False,
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
        del_occ = self.env['calendar.occasion'].sudo().search([('additional_booking', '=', True), ('appointment_id', '=', False)])
        _logger.debug("Removing the following additional occasions: %s" % del_occ)
        del_occ.unlink()
