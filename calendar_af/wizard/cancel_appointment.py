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

from odoo import api, fields, models, _
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class CancelAppointment(models.TransientModel):
    _name = "calendar.cancel_appointment"
    _description = "Cancel appointment"

    @api.model
    def _get_appointments(self):
        return self.env["calendar.appointment"].browse(self._context.get("active_ids"))

    appointment_ids = fields.Many2many(
        string="Appointments to be cancelled",
        comodel_name="calendar.appointment",
        default=_get_appointments,
    )
    cancel_reason = fields.Many2one(
        string="Reason for cancellation",
        comodel_name="calendar.appointment.cancel_reason",
    )

    def action_cancel_appointment(self):
        if self.cancel_reason:
            return self.appointment_ids.cancel(self.cancel_reason)
