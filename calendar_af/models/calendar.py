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
# RESERVED_TIMEOUT is the default time before a reservation times out.
RESERVED_TIMEOUT = 300.0

# Termer
# appointment = faktiskt bokat möte
# occasions = bokningsbara tider
# schedule = occasions skapas utifrån informationen schedules

# TODO
# clean up _logger.warn messages in the code

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
                    'name': '%sm @ %s' % (schedule.duration, schedule.start.strftime("%Y-%m-%dT%H:%M:%S")),
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

class CalendarAppointmentType(models.Model):
    _name = 'calendar.appointment.type'
    _description = "Meeting type"

    name = fields.Char('Name', required=True)
    ipf_id = fields.Char('IPF Id', required=True, help="The IPF type id, if this is wrong the integration won't work")
    # mötestyps_id
    channel = fields.Many2one(string='Channel', comodel_name='calendar.channel')
    duration = fields.Float(string='Duration')
    ipf_num = fields.Integer(string='IPF Number')
    additional_booking = fields.Boolean(string='Over booking')
    # ärendetyp ace
    # könamn ace
    # standardtid, möte.
    # add competence

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

class CalendarAppointmentSuggestion(models.Model):
    _name = 'calendar.appointment.suggestion'
    _description = "Bookable Occasion"

    appointment_id = fields.Many2one(comodel_name='calendar.appointment', ondelete='cascade')
    start = fields.Datetime()
    stop = fields.Datetime()
    occasion_ids = fields.Many2many(comodel_name='calendar.occasion', string="Occasions")

    @api.multi
    def select_suggestion(self):
        # Kontrollera att occasion_ids fortfarande är lediga
        # Skriv data till appointment_id
        if self.appointment_id.state == 'reserved':
            raise Warning("This appointment is already booked.")
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
                        #('channel', '=', self.channel.id),
                        ('appointment_id', '=', False)
                    ], limit=1)
                if not free_occasion:
                    raise Warning(_("You are screwed."))
                occasions |= free_occasion
        occasions.write({'appointment_id': self.appointment_id.id})
        self.appointment_id.write({
            'state': 'reserved',
            'start': self.start,
            'stop': self.stop,
        })

class CalendarAppointment(models.Model):
    _name = 'calendar.appointment'
    _description = "Appointment"

    name = fields.Char(string='Name', required=True)
    start = fields.Datetime(string='Start', required=True, help="Start date of an appointment")
    stop = fields.Datetime(string='Stop', required=True, help="Stop date of an appointment")
    duration_selection = fields.Selection(string="Duration", selection=[('30 minutes','30 minutes'), ('1 hour','1 hour')])
    duration = fields.Float('Duration')
    user_id = fields.Many2one(string='Case worker', comodel_name='res.users', help="Booked case worker")
    partner_id = fields.Many2one(string='Customer', comodel_name='res.partner', help="Booked customer", default=lambda self: self.default_partners())
    state = fields.Selection(selection=[('free', 'Free'),
                                        ('reserved', 'Reserved'),
                                        ('confirmed', 'Confirmed'),
                                        ('canceled', 'Canceled')],
                                        string='State', 
                                        default='free', 
                                        help="Status of the meeting")
    location_code = fields.Char(string='Location')
    office = fields.Many2one('res.partner', string="Office", related="partner_id.office")
    office_code = fields.Char(string='Office code', related="office.office_code")
    occasion_ids = fields.One2many(comodel_name='calendar.occasion', inverse_name='appointment_id', string="Occasion")
    type_id = fields.Many2one(string='Type', required=True, comodel_name='calendar.appointment.type')
    channel =  fields.Many2one(string='Channel', required=True, comodel_name='calendar.channel', related='type_id.channel')
    additional_booking = fields.Boolean(String='Over booking', related='occasion_ids.additional_booking')
    reserved = fields.Datetime(string='Reserved', help="Occasions was reserved at this date and time")
    description = fields.Text(string='Description')
    suggestion_ids = fields.One2many(comodel_name='calendar.appointment.suggestion', inverse_name='appointment_id', string='Suggested Dates')
    """ suggestion_id = fields.Many2one(comodel_name='calendar.appointment.suggestion', string='Suggested Dates') """

    @api.model
    def default_partners(self):
        """ When active_model is res.partner, the current partners should be attendees """
        partners = self.env['res.partner']
        active_id = self._context.get('active_id')
        _logger.info("active_id: %s" % active_id)
        if self._context.get('active_model') == 'res.partner' and active_id:
            if active_id not in partners.ids:
                partners |= self.env['res.partner'].browse(active_id)
        _logger.info("partners: %s" % partners)
        return partners
    
    @api.onchange('type_id')
    def set_duration_selection(self):
        if self.type_id.duration == 30.0:
            self.duration_selection = '30 minutes'
        elif self.type_id.duration == 60.0:
            self.duration_selection = '1 hour'
        
    
    @api.onchange('duration_selection')
    def set_duration(self):
        if self.duration_selection == "30 minutes":
            self.duration = 30.0
        if self.duration_selection == "1 hour":
            self.duration = 60.0

    @api.onchange('duration', 'channel')
    def compute_suggestion_ids(self):
        if not all((self.duration, self.type_id, self.channel)):
            return
        start = self.start_meeting_search()
        stop = self.stop_meeting_search(start)
        suggestion_ids = []
        if self.suggestion_ids:
            suggestion_ids.append((5,))
        occasions = self.env['calendar.occasion'].get_bookable_occasions(start, stop, self.duration * 60, self.type_id, max_depth = 1)
        # _logger.warn(occasions)
        for day in occasions:
            for day_occasions in day:
                for occasion in day_occasions:
                    suggestion_ids.append((0, 0, {
                        # Fyll i occasions-data på förslagen
                        'start': occasion[0].start,
                        'stop': occasion[-1].stop,
                        'occasion_ids': [(6, 0, occasion._ids)],
                    }))
        self.suggestion_ids = suggestion_ids
    
    

    @api.onchange('duration', 'start')
    def onchange_duration_start(self):
        if self.start and self.duration:
            self.stop = self.start + timedelta(minutes=int(self.duration * 60)) 

    def start_meeting_search(self):
        start = datetime.now() + timedelta(days=int(self.env['ir.config_parameter'].sudo().get_param('af_calendar.start_meeting_search', default='3')))
        start.replace(hour=BASE_DAY_START.hour, minute=BASE_DAY_START.minute, second=0, microsecond=0)
        return start

    def stop_meeting_search(self, start_meeting_search):
        stop = start_meeting_search + timedelta(days=int(self.env['ir.config_parameter'].sudo().get_param('af_calendar.stop_meeting_search', default='15')))
        stop.replace(hour=BASE_DAY_STOP.hour, minute=BASE_DAY_STOP.minute, second=0, microsecond=0)
        return stop

    def cancel(self, cancel_reason):
        """Cancels a planned meeting"""
        if self.state == 'confirmed':
            self.state = 'canceled'

    def confirm_appointment(self):
        """Confirm reserved booking"""
        if self.state == 'reserved':
            self.state = 'confirmed'
            res = True
        else: 
            res = False

        return res

    # @api.model
    # def create(self, values):
    #     res = False
    #     start = datetime.strptime(values.get('start'), "%Y-%m-%d %H:%M:%S")
    #     stop = datetime.strptime(values.get('stop'), "%Y-%m-%d %H:%M:%S")
    #     duration = values.get('duration') * 60 # convert from hours to minutes
    #     type_id = self.env['calendar.appointment.type'].browse(values.get('type_id'))
    #     occasions = values.get('occasion_ids')
    #     if not occasions:
    #         occasions = self.env['calendar.occasion'].get_bookable_occasions(start, stop, duration, type_id, values.get('channel'))
    #     if occasions:
    #         values['occasion_ids'] =  [(6,0, [occasion.id for occasion in occasions[0]])]
    #     # TODO: query user before moving appointment?
    #     values['start'] = occasions[0][0].start
    #     values['stop'] = occasions[0][len(occasions[0]) - 1].stop
    #     res = super(CalendarAppointment, self).create(values)
    #     return res

    @api.model
    def update(self, values):
        res = False
        start = datetime.strptime(values.get('start'), "%Y-%m-%d %H:%M:%S")
        stop = datetime.strptime(values.get('stop'), "%Y-%m-%d %H:%M:%S")
        duration = values.get('duration') * 60 # convert from hours to minutes
        type_id = self.env['calendar.appointment.type'].browse(values.get('type_id'))

        occasions = self.env['calendar.occasion'].get_bookable_occasions(start, stop, duration, type_id, values.get('channel'))
        if occasions:
            values['occasion_ids'] =  [(6,0, [occasion.id for occasion in occasions[0]])]
            # TODO: query user before moving appointment?
            values['start'] = occasions[0][0].start
            values['stop'] = occasions[0][len(occasions[0]) - 1].stop
            res = super(CalendarAppointment, self).write(values)
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

class CalendarOccasion(models.Model):
    _name = 'calendar.occasion'
    _description = "Occasion"

    name = fields.Char(string='Name', required=True)
    start = fields.Datetime(string='Start', required=True, help="Start date of an occasion")
    stop = fields.Datetime(string='Stop', required=True, help="Stop date of an occasion")
    duration = fields.Float('Duration')
    appointment_id = fields.Many2one(comodel_name='calendar.appointment', string="Appointment")
    type_id = fields.Many2one(comodel_name='calendar.appointment.type', string='Type')
    channel = fields.Many2one(string='Channel', comodel_name='calendar.channel', related='type_id.channel')
    additional_booking = fields.Boolean(String='Over booking')
    user_id = fields.Many2one(string='Case worker', comodel_name='res.users', help="Booked case worker")
    state = fields.Selection(selection=[('request', 'Awaiting acceptance'),
                                        ('ok', 'Ready to book'),
                                        ('fail', 'Denied')],
                                        string='Occasion state', 
                                        default='request', 
                                        help="Status of the meeting")

    @api.model
    def _force_create_occasion(self, duration, start, type_id, channel, state):
        """In case we need to force through a new occasion for some reason"""
        vals = {
            'name': '%sm @ %s' % (duration, start),
            'start': start,
            'stop': start + timedelta(minutes=duration),
            'duration': duration,
            'appointment_id': False,
            'type_id': type_id,
            'channel': channel,
            'additional_booking': True,
            'state': state,
        }
        res = self.env['calendar.occasion'].create(vals)
        return res

    @api.model
    def _get_min_occasions(self, type_id, date_start=None, date_stop=None):
        """Returns the timeslot (as a start date, DateTime) with the least 
        amount of occurances for a specific timeframe"""
        date_start = date_start or copy.copy(BASE_DAY_START)
        date_stop = date_stop or copy.copy(BASE_DAY_STOP)
        loop_date = date_start
        occ_time = {}
        while loop_date < date_stop:
            # _logger.warn("loop_date: %s" % loop_date)
            occ_time[loop_date.strftime("%Y-%m-%dT%H:%M:%S")] = self.env['calendar.occasion'].search_count([('start', '=', loop_date),('type_id', '=', type_id.id)])
            loop_date = loop_date + timedelta(minutes=BASE_DURATION)
        occ_time_min_key = min(occ_time, key=occ_time.get)
        res = datetime.strptime(occ_time_min_key, "%Y-%m-%dT%H:%M:%S")
        return res

    @api.model
    def _check_date_mapping(self, date):
        """Checks if a date has a mapped date, and returns the mapped date 
        if it exists """
        mapped_date = self.env['calendar.mapped_dates'].search([('from_date', '=', date)])
        if mapped_date:
            res = mapped_date.to_date 
        else:
            res = date
        return res

    @api.model
    def _get_additional_booking(self, date, duration, type_id):
        """"Creates extra, additional, occasions. Iff overbooking is allowed. """
        # Check if overbooking is allowed on this meeting type
        if not type_id.additional_booking:
            # TODO: Throw error instead?
            _logger.warn("Overbooking not allowed on %s" % type_id.name) 
            return False
        # Replace date with mapped date if we have one
        date = self._check_date_mapping(date)
        date_list = date.strftime("%Y-%-m-%-d").split("-")
        # Copy to make sure we dont overwrite BASE_DAY_START or BASE_DAY_STOP
        day_start = copy.copy(BASE_DAY_START)
        day_stop = copy.copy(BASE_DAY_STOP)
        # Ugly, ugly code..
        day_start = day_start.replace(year=int(date_list[0]), month=int(date_list[1]), day=int(date_list[2]))
        day_stop = day_stop.replace(year=int(date_list[0]), month=int(date_list[1]), day=int(date_list[2]))
        # Find when to create new occasion
        start_date = self._get_min_occasions(type_id, day_start, day_stop)
        # Calculate how many occasions we need
        no_occasions = int(duration / BASE_DURATION)
        # Create new occasions.
        res = self.env['calendar.occasion']
        # _logger.warn('Additional booking: %s %s %s' % (start_date, duration, no_occasions))
        for i in range(no_occasions):
            vals = {
                'name': '%sm @ %s' % (duration, start_date),
                'start': start_date,
                'stop': start_date + timedelta(minutes=BASE_DURATION),
                'duration': BASE_DURATION,
                'appointment_id': False,
                'type_id': type_id.id,
                'channel': type_id.channel.id,
                'additional_booking': True,
                'state': 'ok',
            }
            # _logger.warn(vals)
            res |= self.env['calendar.occasion'].create(vals)
            start_date = start_date + timedelta(minutes=BASE_DURATION)
        return res

    @api.multi
    def approve_occasion(self):
        """User approves suggested occasion"""
        if self.state == 'request':
            self.state = 'ok'
            ret = True
        else:
            ret = False

        return ret

    @api.multi
    def deny_occasion(self):
        """User denies suggested occasion"""
        if self.state == 'request':
            self.state = 'fail'
            ret = True
        else:
            ret = False

        return ret

    @api.model
    def get_bookable_occasions(self, start, stop, duration, type_id, max_depth = 1):
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
            return self.env['calendar.occasion'].search(
                [
                    ('start', '=', start_dt),
                    ('type_id', '=', type_id.id),
                    ('appointment_id', '=', False)
                ], limit=max_depth)
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
            # if day == 0:
            if day == date_delta.days:
                start_dt = copy.copy(stop)
                start_dt = start_dt.replace(hour=BASE_DAY_START.hour, minute=BASE_DAY_START.minute)
                last_slot = copy.copy(stop)
                last_slot = last_slot.replace(hour=BASE_DAY_STOP.hour, minute=BASE_DAY_STOP.minute)
                # TODO: I commented this if statement and nothing has exploded yet. Remove it completely?
                # if last_slot > stop:
                #     last_slot = copy.copy(stop)
                last_slot -= timedelta(minutes=duration)
            else:
                # This will break given certain times and timezones. Should work for us.
                # start_dt = start_dt + timedelta(days=1)
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
                    # occasions.append(get_occasions(start_dt + td_base_duration * no_occasions))
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
        # TODO: do not create extra occasions unless completely empty?
        if type_id.additional_booking and all( not l for l in occ_lists):
            # Changed this line to create over bookings on the LAST available date.
            # occ_lists[-1].append(self._get_additional_booking(start_dt, duration, type_id))
            occ_lists[-1].append(self._get_additional_booking(stop, duration, type_id))

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
                'location_code': False,
                'office': False,
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
