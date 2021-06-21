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

LOCAL_TZ = 'Europe/Stockholm'


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
                "type": "ir.actions.act_window",
            }
        except:
            pass


class CalendarAppointment(models.Model):
    _inherit = "calendar.appointment"

    @api.multi
    @api.depends("partner_id", "start")
    def name_get(self):
        result = []
        for app in self:
            try:
                name = _("Meeting with %s at %s") % (
                    app.partner_id.company_registry,
                    pytz.timezone(LOCAL_TZ).localize(app.start),
                )
            except:
                name = _("Meeting at %s") % pytz.timezone(LOCAL_TZ).localize(app.start)
            result.append((app.id, name))
        return result

    partner_pnr = fields.Char(
        string="Attendee SSN",
        related="partner_id.company_registry",
        readonly=True,
        groups="af_security.af_jobseekers_officer",
    )


class CalendarOccasion(models.Model):
    _inherit = "calendar.occasion"

    app_partner_pnr = fields.Char(
        string="Attendee SSN",
        related="appointment_id.partner_id.company_registry",
        readonly=True,
    )
