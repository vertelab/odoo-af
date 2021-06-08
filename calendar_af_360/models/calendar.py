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
import pytz
from datetime import datetime

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

LOCAL_TZ = "Europe/Stockholm"


class CalendarAppointmentSuggestion(models.Model):
    _inherit = "calendar.appointment.suggestion"

    @api.multi
    def select_suggestion(self):
        # check state of appointment
        super(CalendarAppointmentSuggestion, self).select_suggestion()
        try:
            # TODO: We should only get here when going through Arbetsyta.
            # When not going through Arbetsyta, jobseeker access can not be guaranteed.
            # This is an ugly hack to prevent read errors when not going through Arbetsyta.
            self.appointment_id.partner_id.name
            return {
                "name": _("Jobseekers"),
                "res_id": self.appointment_id.partner_id.id,
                "res_model": "res.partner",
                "view_id": self.env.ref("partner_view_360.view_jobseeker_form").id,
                "view_mode": "form",
                "target": "main",
                "type": "ir.actions.act_window",
            }
        except:
            pass

    @api.multi
    def select_suggestion_move(self):
        # check state of appointment
        super(CalendarAppointmentSuggestion, self).select_suggestion_move()
        try:
            # TODO: We should only get here when going through Arbetsyta.
            # When not going through Arbetsyta, jobseeker access can not be guaranteed.
            # This is an ugly hack to prevent read errors when not going through Arbetsyta.
            self.appointment_id.partner_id.name
            return {
                "name": _("Jobseekers"),
                "res_id": self.appointment_id.partner_id.id,
                "res_model": "res.partner",
                "view_id": self.env.ref("partner_view_360.view_jobseeker_form").id,
                "view_mode": "form",
                "target": "main",
                "type": "ir.actions.act_window",
            }
        except:
            pass


class CalendarAppointment(models.Model):
    _inherit = "calendar.appointment"

    partner_pnr = fields.Char(
        string="Attendee SSN",
        related="partner_id.social_sec_nr",
        readonly=True,
        groups="af_security.af_jobseekers_officer",
    )
    partner_forbidden_types = fields.Many2many(
        string="Partner forbidden types",
        comodel_name="calendar.appointment.type",
        relation="app_forbidden_type_partner",
        related="partner_id.forbidden_meeting_types",
    )


class CalendarOccasion(models.Model):
    _inherit = "calendar.occasion"

    app_partner_pnr = fields.Char(
        string="Attendee SSN",
        related="appointment_id.partner_id.social_sec_nr",
        readonly=True,
    )
