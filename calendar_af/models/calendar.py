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
import logging

_logger = logging.getLogger(__name__)

# Base duration given by TeleOpti. This is the duration of the calendar.schedule slots. 
# BASE_DURATION = 30.0 

class CalendarSchedule(models.Model):
    _name = 'calendar.schedule'
    _description = "Schedule"

    name = fields.Char(string='Schedule name', required=True)
    start = fields.Datetime(string='Start', required=True, help="Start date of a schedule")
    stop = fields.Datetime(string='Stop', required=True, help="Stop date of a schedule")
    duration = fields.Float('Duration')
    scheduled_agents = fields.Integer(string='Scheduled agents', help="Number of scheduled agents")
    forecasted_agents = fields.Integer(string='Forecasted agents', help="Number of forecasted agents")
    competence = fields.Many2one(string='Competence', comodel_name='calendar.schedule.competence', help="Related competence")
    channel = fields.Char(string='Channel') # Always SPD for now, might change in future.  # TODO: remove hardcoded default in future, change to many2one?

    @api.multi
    def create_occasions(self):
        for schedule in self:
            vals = {
                'name': '%sm @ %s' % (schedule.duration, schedule.start.strftime("%Y-%m-%dT%H:%M:%SZ")),
                'duration': schedule.duration,
                'start': schedule.start,
                'stop': schedule.stop,
                'competence_id': schedule.competence,
                'channel': schedule.channel,
            }
            for occasion in range(schedule.scheduled_agents-1):
                self.env['calendar.occasion'].create(vals)

class CalendarScheduleCompetence(models.Model):
    # TODO: This class should be merged with a generic "competence"-class if we use it in more areas of odoo.
    _name = 'calendar.schedule.competence'
    _description = "Competence"

    name = fields.Char('Competence name', required=True)
    # AF specific attribute
    ipf_id = fields.Char('IPF Id', required=True, help="The IPF competence id, if this is wrong the integration won't work")
    channel = fields.Char(string='Channel')

class CalendarAppointment(models.Model):
    _name = 'calendar.appointment'
    _description = "Appointment"

    ipf_id = fields.Char(string='IPF id', index=True, required=True)
    name = fields.Char(string='Appointment name', required=True)
    start = fields.Datetime(string='Start', required=True, help="Start date of an appointment")
    stop = fields.Datetime(string='Stop', required=True, help="Stop date of an appointment")
    duration = fields.Float('Duration')
    user_id = fields.Many2one(string='Case worker', comodel_name='res.users', help="Booked case worker") #handläggare?
    partner_id = fields.Many2one(string='Customer', comodel_name='res.partner', help="Booked customer")
    status = fields.Char(string='Status')
    location_code = fields.Char(string='Location')
    office = fields.Many2one('res.partner', string="Office")
    office_code = fields.Char(string='Office code', related="office.office_code")
    occasion_id = fields.One2many(comodel_name='calendar.occasion', inverse_name='appointment_id', string="Occasion")
    competence_id = fields.Many2one(string='Type / Competence', related='occasion_id.competence_id')
    channel =  fields.Char(string='Channel', related='occasion_id.channel')

class CalendarOccasion(models.Model):
    _name = 'calendar.occasion'
    _description = "Occasion"

    name = fields.Char(string='Occasion name', required=True)
    start = fields.Datetime(string='Start', required=True, help="Start date of an occasion")
    stop = fields.Datetime(string='Stop', required=True, help="Stop date of an occasion")
    duration = fields.Float('Duration')
    appointment_id = fields.Many2one(comodel_name='calendar.appointment', string="Appointment")
    competence_id = fields.Many2one(comodel_name='calendar.schedule.competence', string='Type / Competence')
    channel = fields.Char(string='Occasion channel')

    def get_bookable_occasion(self):
        res = self.env['calendar.occasion']
        return res

    def reserve_occasion(self):
        res = self.env['calendar.occasion']
        return res
    
    def confirm_appointment(self):
        res = self.env['calendar.appointment']
        return res