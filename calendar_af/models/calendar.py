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
import logging

_logger = logging.getLogger(__name__)

# TODO: decide if we are dependent on this variable or the imported schedule duration.
# Base duration given by TeleOpti. This is the duration of the calendar.schedule slots in minutes.
BASE_DURATION = 30.0 

class CalendarSchedule(models.Model):
    _name = 'calendar.schedule'
    _description = "Schedule"

    name = fields.Char(string='Name', required=True)
    start = fields.Datetime(string='Start', required=True, help="Start date of a schedule")
    stop = fields.Datetime(string='Stop', required=True, help="Stop date of a schedule")
    duration = fields.Float('Duration')
    scheduled_agents = fields.Integer(string='Scheduled agents', help="Number of scheduled agents")
    forecasted_agents = fields.Integer(string='Forecasted agents', help="Number of forecasted agents")
    competence = fields.Many2one(string='Competence', comodel_name='calendar.schedule.competence', help="Related competence")
    channel = fields.Char(string='Channel')

    @api.multi
    def create_occasions(self):
        for schedule in self:
            vals = {
                'name': '%sm @ %s' % (schedule.duration, schedule.start.strftime("%Y-%m-%dT%H:%M:%S")),
                'duration': schedule.duration,
                'start': schedule.start,
                'stop': schedule.stop,
                'competence_id': schedule.competence.id,
                'channel': schedule.channel,
            }
            for occasion in range(schedule.scheduled_agents):
                self.env['calendar.occasion'].create(vals)

class CalendarScheduleCompetence(models.Model):
    # TODO: This class should be merged with a generic "competence"-class if we use it in more areas of odoo.
    _name = 'calendar.schedule.competence'
    _description = "Competence"

    name = fields.Char('Name', required=True)
    # AF specific attribute
    ipf_id = fields.Char('IPF Id', required=True, help="The IPF competence id, if this is wrong the integration won't work")
    channel = fields.Char(string='Channel')

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
    competence_id = fields.Many2one(string='Type / Competence', related='occasion_ids.competence_id')
    channel =  fields.Char(string='Channel', related='occasion_ids.channel')
    over_booking = fields.Boolean(String='Over booking', related='occasion_ids.over_booking')

class CalendarOccasion(models.Model):
    _name = 'calendar.occasion'
    _description = "Occasion"

    name = fields.Char(string='Name', required=True)
    start = fields.Datetime(string='Start', required=True, help="Start date of an occasion")
    stop = fields.Datetime(string='Stop', required=True, help="Stop date of an occasion")
    duration = fields.Float('Duration')
    appointment_id = fields.Many2one(comodel_name='calendar.appointment', string="Appointment")
    competence_id = fields.Many2one(comodel_name='calendar.schedule.competence', string='Type / Competence')
    channel = fields.Char(string='Channel')
    over_booking = fields.Boolean(String='Over booking')

    def _force_create_occasion(self, duration, start, competence, channel):
        vals = {
            'name': '%sm @ %s' % (duration, start),
            'start': start,
            'stop': start + timedelta(minutes=duration),
            'duration': duration,
            'appointment_id': False,
            'competence_id': competence,
            'channel': channel,
            'over_booking': True,
        }
        res = self.env[calendar.occasion].create(vals)
        return res

    # TODO: add duration as argument
    def get_bookable_occasion(self, start, stop, competence, channel, max_depth = 1):
        # Calculate number of occasions needed to match booking duration
        no_occasions = int((stop - start) / timedelta(minutes=BASE_DURATION))

        # TODO: decide on method #1 or #2. #2 seems less expensive.  
        # # START METHOD #1 (probably contains bugs)
        # occ_lists = {}
        # # repeat search per depth
        # for i in range(max_depth):
        #     iteration_start = start
        #     occasion_ids = []
        #     # find a free occasion for each timeslot
        #     for j in range(no_occasions):
        #         iteration_start = iteration_start + timedelta(minutes=BASE_DURATION) * j
        #         occasion_ids += self.env['calendar.occasion'].search([('start', '=', iteration_start), ('competence_id', '=', competence), ('channel', '=', channel), ('appointment_id', '=', False)], limit=1)

        #     # Creates a dict of lists of occasions to match the appointment duration
        #     occ_lists[i] = occasion_ids
        # # END METHOD #1

        # START METHOD #2
        occ_lists = []
        # not sure if this is needed...
        for i in range(max_depth):
            occ_lists.append([])

        # find 'no_occasions' number of free occasions for each timeslot
        for i in range(no_occasions):
            iteration_start = start + timedelta(minutes=BASE_DURATION) * i
            occasion_ids = self.env['calendar.occasion'].search([('start', '=', iteration_start), ('competence_id', '=', competence), ('channel', '=', channel), ('appointment_id', '=', False)], limit=max_depth)
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
        # END METHOD #2

        # Do we need to make sure that we always deliver bookable occasions here?

        _logger.warn("DAER: get_bookable_occasion return: %s" % occ_lists)
        return occ_lists 

        res = self.env['calendar.occasion']
        return res

    def reserve_occasion(self, occasion_ids):
        start = occasion_ids[0].start
        stop = occasion_ids[len(occasion_ids)-1].stop
        duration = stop.minute - start.minute 
        
        # check that occasions are unreserved
        free = True
        for occasion_id in occasion_ids:
            if occasion_id.appointment_id:
                free = False

        if free:
            vals = {
                'name': occasion_ids[0].competence_id.name,
                'start': start,
                'stop': stop,
                'duration': duration,
                'user_id': False,
                'partner_id': False,
                'status': 'Reserved',
                'location_code': False,
                'office': False,
                'occasion_ids': occasion_ids,
            }
            appointment = self.env['calendar.appointment'].create(vals)

            for occasion_id in occasion_ids:
                occasion_id.appointment_id = appointment.id

            res = appointment
        else:
            # TODO: implement error codes..
            res = '200'

        _logger.warn("DAER: reserve_occasion return: %s" % res)
        return res
    
    def confirm_appointment(self):
        res = self.env['calendar.appointment']
        return res