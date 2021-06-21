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

import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class hr_operation(models.Model):
    _inherit = "hr.operation"

    reserve_admin_ids = fields.Many2many(
        comodel_name="hr.employee",
        string="Reserve time managers",
        relation="hr_operation_hr_employee_reserve",
    )

    app_warn_emp_ids = fields.Many2many(
        comodel_name="hr.employee", string="Appointment warnings"
    )
    type_operation_ids = fields.One2many(
        comodel_name="calendar.appointment.type.operation",
        inverse_name="operation_id",
        string="Type - Operation mapping",
    )
    mapped_dates_ids = fields.One2many(
        comodel_name="calendar.mapped_dates",
        inverse_name="operation_id",
        string="Mapped dates",
    )

    def view_reserve_dates(self):
        return {
            "name": _("Mapped dates for %s") % (self.display_name),
            "res_model": "calendar.mapped_dates",
            "view_type": "form",
            "view_mode": "tree",
            "domain": "[('operation_id', '=', %s)]" % self.id,
            "view_id": self.env.ref("calendar_af.view_calendar_mapped_dates_tree").id,
            "target": "current",
            "type": "ir.actions.act_window",
        }


class AppointmentTypeOperation(models.Model):
    _name = "calendar.appointment.type.operation"
    _description = "Calendar Appointment Type Operation"

    type_id = fields.Many2one(
        comodel_name="calendar.appointment.type",
        string="Appointment type",
        required=True,
    )
    operation_id = fields.Many2one(
        comodel_name="hr.operation", string="Operation", required=True
    )
    warning_threshold = fields.Integer(string="Warning threshold")
