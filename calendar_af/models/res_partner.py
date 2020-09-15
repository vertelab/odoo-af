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
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    appointment_ids_past = fields.One2many(comodel_name='calendar.appointment', string='Booked meetings', compute="compute_show_dates_past")
    appointment_ids_ahead = fields.One2many(comodel_name='calendar.appointment', string='Booked meetings', compute="compute_show_dates_ahead")
    appointment_ids = fields.One2many(comodel_name='calendar.appointment', string='Booked meetings', inverse_name="partner_id")

    @api.one
    def _compute_appointment_count(self):
        for partner in self:
            partner.appointment_count = len(partner.appointment_ids)

    appointment_count = fields.Integer(compute='_compute_appointment_count')

    @api.multi
    def view_appointments(self):
        return{
            'name': _('Booked meetings'),
            'domain':[('partner_id', '=', self.ids)],
            'view_type': 'form',
            'res_model': 'calendar.appointment',
            'view_id': self.env.ref('calendar_af.view_calendar_appointment_tree').id,
            'view_mode': 'tree', 
            'type': 'ir.actions.act_window',
        }


    @api.multi
    def open_partner_calendar(self):
        return{
            'name': _('Calendar'),
            'domain':[('partner_id', '=', self.ids)],
            'view_type': 'form',
            'res_model': 'calendar.appointment',
            'view_id':  False,
            'view_mode': 'tree,calendar,kanban,pivot,form',
            'type': 'ir.actions.act_window',
        }

    #unbook meeting?
    @api.multi
    def create_appointment(self):
        return{
            'name': _('Booked meetings'),
            'domain':[('partner_id', '=', self.ids)],
            'view_type': 'form',
            'res_model': 'calendar.appointment',
            'view_id': self.env.ref('calendar_af.view_calendar_appointment_form').id,
            'view_mode': 'form', 
            'type': 'ir.actions.act_window',
        }

    @api.one
    def compute_show_dates_ahead(self):
        self.appointment_ids_ahead = self.appointment_ids.filtered(lambda a: a.start > datetime.now())
    
    @api.one
    def compute_show_dates_past(self):
        self.appointment_ids_past = self.appointment_ids.filtered(lambda a: a.start < datetime.now())

    @api.model
    def send_to_stom_track(self, pnr_list):
        # pnr_list = [{'pnr': '20000202-2382'}, {'pnr': '20000105-2380'}, {'pnr': '20000203-2399'}, {'foo': 'bar' }]
        pnr_domain = []
        for pnr in pnr_list:
            pnr_domain.append(pnr.get('pnr'))
        # get partners from pnr
        partner_ids = self.env['res.partner'].sudo().search([('company_registry', 'in', pnr_domain)])
        # find our appointment types
        type_21 = self.env.ref('calendar_meeting_type.type_21')
        type_26 = self.env.ref('calendar_meeting_type.type_26')
        # find appointments that need to be moved
        appointment_ids = self.env['calendar.appointment'].search([('partner_id', 'in', partner_ids._ids),('type_id', '=', type_21.id)])
        
        desired_time = datetime.now()
        # loop through appointments to be moved
        for appointment in appointment_ids:
            appointment_length = appointment.duration 
            office = appointment.office
            # find free occasions for meeting type 26
            occasions = self.env['calendar.occasion'].sudo().get_bookable_occasions(desired_time, desired_time + timedelta(appointment_length), appointment_length, type_26, office, 1)
            # loop result until we find a free occasion
            for book_occasion in occasions:
                if book_occasion and book_occasion[0]:
                    # move the appointment
                    res = appointment.move_appointment(book_occasion[0])
                    break
