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
from datetime import timedelta

from odoo import models, fields, api, _
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    appointment_ids = fields.One2many(
        comodel_name="calendar.appointment",
        string="Booked meetings",
        inverse_name="user_id",
    )

    @api.one
    def _compute_appointment_count(self):
        for user in self:
            user.appointment_count = len(user.appointment_ids)

    appointment_count = fields.Integer(compute="_compute_appointment_count")

    @api.multi
    def view_appointments(self):
        return {
            "name": _("Booked meetings"),
            "domain": [("user_id", "=", self.ids)],
            "view_type": "form",
            "res_model": "calendar.appointment",
            "view_id": self.env.ref("calendar_af.view_calendar_appointment_tree").id,
            "view_mode": "tree",
            "type": "ir.actions.act_window",
        }

    def _compute_free_occasions(self):
        return self.env["calendar.occasion"].search(
            [("user_id", "=", self.id), ("appointment_id", "=", False)]
        )

    free_occ = fields.Many2one(
        comodel_name="calendar.occasion",
        string="Free occasions",
        compute=_compute_free_occasions,
    )

    def action_calendar_local_occasion(self):
        res = self.env.ref("calendar_af.action_calendar_local_occasion").read()[0]
        res["domain"] = [
            ("operation_id", "in", self.operation_ids._ids),
            ("user_id", "=", self.id),
            ("state", "!=", "deleted"),
        ]
        return res

    def create_local_occasion_action(self):
        res = self.env.ref("calendar_af.create_local_occasion_action").read()[0]

        # we get context as a str not a dict
        context = eval(res.get("context", "{}"))
        if not self.operation_ids:
            raise Warning(_("User is not connected to any operations"))
        context["default_operation_id"] = self.operation_ids._ids[0]
        context["default_user_ids"] = self._ids
        # convert back to str and return
        res["context"] = str(context)
        return res

    def action_local_appointment(self):
        res = self.env.ref("calendar_af.action_local_appointment").read()[0]
        res["domain"] = [
            ("operation_id", "in", self.operation_ids._ids),
            ("user_id", "=", self.id),
            ("state", "!=", "canceled"),
        ]
        return res

    def check_resource_calendar_occasion(self, check_datetime):
        # We will assume that each user only 
        # has one employee connected for now.
        # TODO: This should be reviewed in the future.
        if self.employee_ids and self.employee_ids[0].resource_calendar_id:
            count_work_hours = self.employee_ids[0].resource_calendar_id.get_work_hours_count(check_datetime, check_datetime + timedelta(minutes=30))
            if count_work_hours == 0.5:
                return True
            else:
                return False
        else:
            # TODO: add raise Warning here?
            # this will stop the system from creating any occasions if so.
            return False
