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
from datetime import datetime, timedelta
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
    channel = fields.Char(string='Channel')

    @api.multi
    def create_occasions(self):
        for schedule in self:
            no_occasions = self.env['calendar.occasion'].search_count([('start', '=', schedule.start), ('type_id', '=', schedule.type_id.id), ('additional_booking', '=', False)])
            if (schedule.scheduled_agents - no_occasions) > 0:
                vals = {
                    'name': '%sm @ %s' % (schedule.duration, schedule.start.strftime("%Y-%m-%dT%H:%M:%S")),
                    'duration': schedule.duration,
                    'start': schedule.start,
                    'stop': schedule.stop,
                    'type_id': schedule.type_id.id,
                    'channel': schedule.channel,
                    'additional_booking': False,
                }
                for occasion in range(schedule.scheduled_agents - no_occasions):
                    self.env['calendar.occasion'].create(vals)

            elif (schedule.scheduled_agents - no_occasions) < 0:
                pass

class CalendarAppointmentType(models.Model):
    _name = 'calendar.appointment.type'
    _description = "Meeting type"

    name = fields.Char('Name', required=True)
    # AF specific attribute
    ipf_id = fields.Char('IPF Id', required=True, help="The IPF type id, if this is wrong the integration won't work")
    channel = fields.Char(string='Channel')
    ipf_num = fields.Integer(string='IPF Number')
    additional_booking = fields.Boolean(string='Over booking')

class CalendarMappedDates(models.Model):
    _name = 'calendar.mapped_dates'
    _description = "Mapped dates"

    name = fields.Char(string="Name")
    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)

class CalendarAppointment(models.Model):
    _name = 'calendar.appointment'
    _description = "Appointment"

    name = fields.Char(string='Name', required=True)
    start = fields.Datetime(string='Start', required=True, help="Start date of an appointment")
    stop = fields.Datetime(string='Stop', required=True, help="Stop date of an appointment")
    duration = fields.Float('Duration')
    user_id = fields.Many2one(string='Case worker', comodel_name='res.users', help="Booked case worker") #handläggare?
    partner_id = fields.Many2one(string='Customer', comodel_name='res.partner', help="Booked customer")
    status = fields.Char(string='Status')
    location_code = fields.Char(string='Location')
    office = fields.Many2one('res.partner', string="Office")
    office_code = fields.Char(string='Office code', related="office.office_code")
    occasion_ids = fields.One2many(comodel_name='calendar.occasion', inverse_name='appointment_id', string="Occasion")
    type_id = fields.Many2one(string='Type', related='occasion_ids.type_id')
    channel =  fields.Char(string='Channel', related='occasion_ids.channel')
    additional_booking = fields.Boolean(String='Over booking', related='occasion_ids.additional_booking')

class CalendarOccasion(models.Model):
    _name = 'calendar.occasion'
    _description = "Occasion"

    name = fields.Char(string='Name', required=True)
    start = fields.Datetime(string='Start', required=True, help="Start date of an occasion")
    stop = fields.Datetime(string='Stop', required=True, help="Stop date of an occasion")
    duration = fields.Float('Duration')
    appointment_id = fields.Many2one(comodel_name='calendar.appointment', string="Appointment")
    type_id = fields.Many2one(comodel_name='calendar.appointment.type', string='Type')
    channel = fields.Char(string='Channel')
    additional_booking = fields.Boolean(String='Over booking')

    def _force_create_occasion(self, duration, start, type_id, channel):
        vals = {
            'name': '%sm @ %s' % (duration, start),
            'start': start,
            'stop': start + timedelta(minutes=duration),
            'duration': duration,
            'appointment_id': False,
            'type_id': type_id,
            'channel': channel,
            'additional_booking': True,
        }
        res = self.env[calendar.occasion].create(vals)
        return res

    def _get_min_occasions(self, type_id, date_start=None, date_stop=None):
        """Returns the timeslot (as a start date, DateTime) with the least 
        amount of occurances for a specific timeframe"""
        date_start = date_start or BASE_DAY_START
        date_stop= date_stop or BASE_DAY_STOP
        go = True
        loop_date = date_start
        occ_time = {}
        while go:
            occ_time[loop_date.strftime("%Y-%m-%dT%H:%M:%S")] = self.env['calendar.occasion'].search_count([('start', '=', loop_date),('type_id', '=', type_id)])
            loop_date = loop_date + timedelta(minutes=BASE_DURATION)
            if loop_date >= date_stop:
                go = False
        occ_time_min_key = min(occ_time, key=occ_time.get)
        res = datetime.strptime(occ_time_min_key, "%Y-%m-%dT%H:%M:%S")
        return res

    def _check_date_mapping(self, date):
        """Checks if a date has a mapped date, and returns the mapped date 
        if it exists """
        mapped_date = self.env['calendar.mapped_dates'].search([('from_date', '=', date)])
        if mapped_date:
            res = mapped_date.to_date 
        else:
            res = date
        return res

    def _get_additional_booking(self, date, duration, type_id):
        # Replace date with mapped date if we have one
        date = self._check_date_mapping(date)
        date_list = date.strftime("%Y-%-m-%-d").split("-")
        # Copy to make sure we dont overwrite BASE_DAY_START or BASE_DAY_STOP
        day_start = copy.copy(BASE_DAY_START)
        day_stop = copy.copy(BASE_DAY_STOP)
        # Ugly, ugly code..
        day_start.replace(year=int(date_list[0]), month=int(date_list[1]), day=int(date_list[2]))
        day_stop.replace(year=int(date_list[0]), month=int(date_list[1]), day=int(date_list[2]))
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
                'duration': BASE_DURATION,
                'appointment_id': False,
                'type_id': type_id,
                'additional_booking': True,
            }
            res |= self.env['calendar.occasion'].create(vals)
            start_date = start_date + timedelta(minutes=BASE_DURATION)
        return res

    # TODO: add duration as argument
    def get_bookable_occasions(self, start, stop, type_id, channel, max_depth = 1):
        # Calculate number of occasions needed to match booking duration
        no_occasions = int((stop - start) / timedelta(minutes=BASE_DURATION))
        # TODO: Return max_depth occasions per slot
        # TODO: Sort return by last date first, add for-loop on date first.

        occ_lists = []
        # declare lists...
        for i in range(max_depth):
            occ_lists.append([])

        # find 'no_occasions' number of free occasions for each timeslot
        for i in range(no_occasions):
            iteration_start = start + timedelta(minutes=BASE_DURATION) * i
            occasion_ids = self.env['calendar.occasion'].search([('start', '=', iteration_start), ('type_id', '=', type_id.id), ('channel', '=', channel), ('appointment_id', '=', False)], limit=max_depth)
            # save one result from each timeslot in a seperate list 
            for j in range(len(occasion_ids)):
                occ_lists[j] += occasion_ids[j]

        # Remove partial matches, these are unusable
        i = 0
        while i < len(occ_lists):
            if len(occ_lists[i]) != no_occasions:
                del occ_lists[i]
            else:
                i += 1

        res = occ_lists
        # if type allows additional bookings and  we didn't find any 
        # free occasions, create new ones:
        if type_id.additional_booking and not res:
            res = self._get_additional_booking(start, stop, type_id, channel)

        return res

    def reserve_occasion(self, occasion_ids):
        start = occasion_ids[0].start
        stop = occasion_ids[len(occasion_ids)-1].stop
        duration = stop.minute - start.minute 

        # TODO: Reserve-booking = TRANSIENT MODEL?, reservations are kept for 5 minutes
        # 5 minutes should be a changeable parameter = not transient model..?

        # check that occasions are unreserved
        free = True
        for occasion_id in occasion_ids:
            if occasion_id.appointment_id:
                free = False

        if free:
            vals = {
                'name': occasion_ids[0].type_id.name,
                'start': start,
                'stop': stop,
                'duration': duration,
                'user_id': False,
                'partner_id': False,
                'status': 'Reserved',
                'location_code': False,
                'office': False,
                'occasion_ids': occasion_ids, # I dont think this does anything?
            }
            appointment = self.env['calendar.appointment'].create(vals)

            # relation needs to be set from calendar.occasion 
            for occasion_id in occasion_ids:
                occasion_id.appointment_id = appointment.id

            res = appointment
        else:
            # TODO: implement error codes..
            res = '200' # 400, 403, 404, 500

        return res

    def confirm_appointment(self):
        res = self.env['calendar.appointment']
        return res
