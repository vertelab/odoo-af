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

from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class HrOperation(models.Model):
    _inherit = "hr.operation"

    user_ids = fields.Many2many(comodel_name="res.users", compute="compute_user_ids")
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
    reserve_time = fields.Float(string="Reserve time start")
    af_show_in_tree = fields.Boolean(compute="_compute_af_show_in_tree",
                                     search="_search_af_show_in_tree",
                                     help="Whether this operation should show up in"
                                          "the standard list view.")
    is_office_manager = fields.Boolean(
        string="Is office manager", compute="_compute_is_office_manager")

    def _compute_af_show_in_tree(self):
        """Not needed. We only want to search."""
        pass

    def _search_af_show_in_tree(self, op, value):
        """ Meeting Admin should see every operation.
        Other users should only see their own offices."""
        if op != "=":
            raise Warning(_("%s operator not implemented for hr.operation.af_show_in_tree!") % op)
        if value is not True:
            raise Warning(_("Value '%s' not implemented for hr.operation.af_show_in_tree!") % op)
        if self.env.user.has_group("base.group_system"):
            return []
        if self.env.user.has_group("af_security.af_meeting_admin"):
            return []
        return [("id", "in", self.env.user.mapped("employee_ids.office_ids.id"))]

    def _compute_is_office_manager(self):
        self.is_office_manager = (
                self.env.user.has_group("af_security.af_meeting_admin") or
                self.env.user.has_group("base.group_system")
        )

    @api.one
    def compute_user_ids(self):
        for employee in self.employee_ids:
            self.user_ids |= employee.user_id

    def view_reserve_dates(self):
        return {
            "name": _("Mapped dates for %s") % self.display_name,
            "res_model": "calendar.mapped_dates",
            "view_type": "form",
            "view_mode": "tree",
            "domain": "[('operation_id', '=', %s)]" % self.id,
            "view_id": self.env.ref("calendar_af.view_calendar_mapped_dates_tree").id,
            "target": "current",
            "type": "ir.actions.act_window",
        }

    @api.multi
    def open_users_tree(self):
        res = self.env["ir.actions.act_window"].for_xml_id(
            "calendar_af", "action_calendar_user"
        )
        context = eval(res.get("context", "{}"))
        context["default_operation_id"] = self.id
        res["context"] = str(context)
        if self.user_ids:
            res["domain"] = [("id", "in", self.user_ids._ids)]
        else:
            raise ValidationError(_("No administrative officers on this operation"))
        return res

    def _check_employee_ids_access(self):
        """Allow Meeting admins to write employees."""
        if self.env.user.has_group('af_security.af_meeting_admin'):
            return True
        return super(HrOperation, self)._check_employee_ids_access()


class AppointmentTypeOperation(models.Model):
    _name = "calendar.appointment.type.operation"

    type_id = fields.Many2one(
        comodel_name="calendar.appointment.type",
        string="Appointment type",
        required=True,
        index=True,
    )
    operation_id = fields.Many2one(
        comodel_name="hr.operation", string="Operation", required=True, index=True
    )
    warning_threshold = fields.Integer(string="Warning threshold")
