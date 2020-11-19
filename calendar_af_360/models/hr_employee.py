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
from datetime import datetime

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    appointment_ids_ahead = fields.One2many(
        comodel_name="calendar.appointment",
        string="Booked meetings ahead",
        compute="_get_records",
    )

    appointment_ids = fields.One2many(
        comodel_name="calendar.appointment",
        string="Booked meetings",
        inverse_name="user_id",
        compute="_get_records",
    )
    appointment_ids_all = fields.One2many(
        comodel_name="calendar.appointment",
        string="Booked meetings ahead for everyone",
        inverse_name="user_id",
        compute="_get_records",
    )

    @api.depends("user_id")
    def _get_records(self):
        for rec in self:
            if not rec.user_id:
                continue
            appointment_record = rec.env["calendar.appointment"].search(
                [("user_id", "=", rec.user_id.id)]
            )
            rec.appointment_ids = appointment_record
            rec.appointment_ids_ahead = appointment_record.filtered(
            lambda a: a.start > fields.datetime.now() and a.state == "confirmed" #datetime.now() might not work?
            )

            appointment_record = rec.env["calendar.appointment"].search(
                [
                    ("user_id", "!=", rec.user_id.id),
                    ("office_id", "in", rec.user_id.office_ids._ids),
                ]
            )

            rec.appointment_ids_all = appointment_record.filtered(
                lambda a: a.start > fields.datetime.now()
                and a.state == "confirmed"
            )


class HrEmployeeJobseekerSearchWizard(models.TransientModel):
    _inherit = "hr.employee.jobseeker.search.wizard"

    appointment_ids_ahead = fields.One2many(related="employee_id.appointment_ids_ahead")

    appointment_ids_all = fields.One2many(related="employee_id.appointment_ids_all")

    @api.multi
    def create_appointment(self):
        return {
            "name": _("Booked meetings"),
            "domain": [("partner_id", "=", self.ids)],
            "view_type": "form",
            "res_model": "calendar.appointment",
            "view_id": self.env.ref("calendar_af.view_calendar_appointment_form").id,
            "view_mode": "form",
            "type": "ir.actions.act_window",
        }

    @api.multi
    def open_others_appointments_ahead(self):
        return {
            "name": _("Calendar"),
            "domain": [
                ("start", ">", datetime.now()),
                ("user_id", "!=", self.env.user.id),
                ("office_id", "in", self.env.user.office_ids._ids),
            ],
            "view_type": "form",
            "res_model": "calendar.appointment",
            "view_id": False,
            "view_mode": "tree,calendar,form",
            "type": "ir.actions.act_window",
        }
