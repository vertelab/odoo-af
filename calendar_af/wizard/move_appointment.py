# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2021 Vertel AB (<http://vertel.se>).
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
from odoo.exceptions import UserError
import logging


_logger = logging.getLogger(__name__)


class MoveAppointment(models.TransientModel):
    _name = "calendar.move_appointment"
    _description = "Move appointment"

    @api.model
    def _get_appointment(self):
        app_id = self._context.get("active_id")
        if not app_id:
            raise UserError(_("No appointment selected."))
        return self.env["calendar.appointment"].browse(app_id)

    @api.model
    def _get_channel(self):
        app_id = self._context.get("active_id")
        if not app_id:
            raise UserError(_("No appointment selected."))
        app = self.env["calendar.appointment"].browse(app_id)
        return app.channel

    @api.model
    def _get_type(self):
        app_id = self._context.get("active_id")
        if not app_id:
            raise UserError(_("No appointment selected."))
        app = self.env["calendar.appointment"].browse(app_id)
        app.suggestion_ids = False
        app.show_suggestion_ids = False
        return app.type_id

    @api.model
    def _get_operation(self):
        app_id = self._context.get("active_id")
        if not app_id:
            raise UserError(_("No appointment selected."))
        app = self.env["calendar.appointment"].browse(app_id)
        return app.operation_id

    appointment_id = fields.Many2one(
        string="Appointment to be moved",
        comodel_name="calendar.appointment",
        default=_get_appointment,
    )
    move_reason = fields.Many2one(
        string="Reason for move",
        comodel_name="calendar.appointment.cancel_reason",
    )
    state = fields.Selection(related="appointment_id.state")
    name = fields.Char(related="appointment_id.name")
    channel = fields.Many2one(comodel_name="calendar.channel", default=_get_channel)
    type_id = fields.Many2one(
        comodel_name="calendar.appointment.type", default=_get_type
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner", related="appointment_id.partner_id"
    )
    user_id = fields.Many2one(
        comodel_name="res.users", related="appointment_id.user_id"
    )
    start = fields.Datetime(related="appointment_id.start")
    stop = fields.Datetime(related="appointment_id.stop")
    cancel_reason_temp = fields.Many2one(
        string="Cancel reason",
        comodel_name="calendar.appointment.cancel_reason",
        # store=False,
        help="Cancellation reason",
    )
    operation_id = fields.Many2one(
        comodel_name="hr.operation", default=_get_operation
    )
    office_id = fields.Many2one(
        comodel_name="hr.department",
        related="appointment_id.office_id",
    )
    suggestion_ids = fields.One2many(
        comodel_name="calendar.appointment.suggestion",
        # string="Suggestions",
        related="appointment_id.suggestion_ids",
    )
    show_suggestion_ids = fields.Boolean(
        # string="Show suggestions",
        related="appointment_id.show_suggestion_ids",
    )

    def compute_suggestion_ids(self):

        # store values from appointment_id
        old_channel = self.appointment_id.channel
        old_operation =self.operation_id
        old_type = self.appointment_id.type_id
        old_duration = self.appointment_id.duration
        # update appointment_id with data from wizard
        self.appointment_id.channel = self.channel
        self.appointment_id.operation_id = self.operation_id
        self.appointment_id.type_id = self.type_id
        self.appointment_id.duration = self.type_id.duration / 60
        self.appointment_id.cancel_reason = self.cancel_reason_temp
        # get new times
        self.appointment_id.compute_suggestion_ids()
        # update wizard values
        self.show_suggestion_ids = True
        self.suggestion_ids = self.appointment_id.suggestion_ids
        # Restore data on appointment_id in case the user aborts the move before selecting a time.
        self.appointment_id.channel = old_channel
        self.appointment_id.operation_id = old_operation
        self.appointment_id.type_id = old_type
        self.appointment_id.duration = old_duration

        # keep the wizard open, but reload the form
        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'calendar.move_appointment',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'inline',
        }
