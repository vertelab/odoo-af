# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2019 Vertel AB (<http://vertel.se>).
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

import json
import logging
from datetime import datetime
import time
from zeep.client import CachingClient

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, Warning
from odoo.http import request

import requests

_logger = logging.getLogger(__name__)
TIMEOUT = 60 * 3


def validate_personnummer(ssnid):
    control_digit = int(ssnid[-1])
    tot = 0
    multiplicator = 2
    for digit in ssnid[:-1]:
        res = int(digit) * multiplicator
        if res > 9:
            res = 1 + res % 10
        tot += res
        multiplicator = (multiplicator % 2) + 1
    return (10 - (tot % 10)) % 10 == control_digit


class HrEmployeeJobseekerSearchWizard(models.TransientModel):
    _name = "hr.employee.jobseeker.search.wizard"

    @api.model
    def _get_default_social_sec_nr_search(self):
        ssn_not_found = request.session.pop("ssn_not_found", False)
        ssn = request.session.pop("ssn", "")
        if ssn_not_found:
            ssn = _("%s [This jobseeker is not registered at Arbetsförmedlingen]") % ssn
        return ssn

    employee_id = fields.Many2one(
        comodel_name="hr.employee", default=lambda self: self._default_hr_employee()
    )
    jobseekers_ids = fields.One2many("res.partner", compute="_get_records")

    # this may be used in the future, but in that case move this code to partner_daily_notes and the partner_af_case module respectively instead
    # case_ids = fields.One2many('res.partner.case', compute='_get_records')
    # daily_note_ids = fields.One2many('res.partner.notes', compute='_get_records')
    # Looks like related doesn't work on computed fields :(
    # jobseekers_ids = fields.One2many(related='employee_id.jobseekers_ids')
    # case_ids = fields.One2many(related='employee_id.case_ids')
    # daily_note_ids = fields.One2many(related='employee_id.daily_note_ids')

    social_sec_nr_search = fields.Char(
        string="Social security number",
        default=lambda self: "%s" % self._get_default_social_sec_nr_search(),
        help="It's also possible to search for co-ordination number"
    )
    bank_id_text = fields.Text(string=None)
    bank_id_ok = fields.Boolean(string=None, default=False)

    search_reason = fields.Selection(
        string="Search reason",
        selection=[
            ("record incoming documents", "Record incoming documents"),
            (
                "follow-up of job seekers' planning",
                "Follow-up of job seekers' planning",
            ),
            ("directory Assistance", "Directory Assistance"),
            ("matching", "Matching"),
            ("decisions for other officer", "Decisions for other officer"),
            (
                "administration of recruitment meeting/group activity/project",
                "Administration of recruitment meeting/group activity/project",
            ),
            ("investigation", "Investigation"),
            ("callback", "Callback"),
            ("other reason", "Other reason"),
        ],
    )  #
    identification = fields.Selection(
        string="Identification",
        selection=[
            ("id document", "ID document"),
            ("Digital ID", "Digital ID"),
            (
                "id document-card/residence permit card",
                "ID document-card/Residence permit card",
            ),
            ("known (previously identified)", "Known (previously identified)"),
            ("identified by certifier", "Identified by certifier"),
        ],
    )  #

    customer_id_search = fields.Char(string="Customer number")
    email_search = fields.Char(string="Email")

    search_domain = fields.Char(string="Search Filter")
    other_reason = fields.Char(string="Other reason")

    @api.depends("employee_id")
    def _get_records(self):
        for rec in self:
            if rec.employee_id.user_id:
                rec.jobseekers_ids = rec.env["res.partner"].search(
                    [("user_id", "=", rec.employee_id.user_id.id)]
                )
                # rec.case_ids = rec.env['res.partner.case'].search([('administrative_officer', '=', rec.employee_id.user_id.id)])
                # rec.daily_note_ids = rec.env['res.partner.notes'].search(
                #    [('administrative_officer', '=', rec.employee_id.user_id.id)])

    def _default_hr_employee(self):
        return self.env.user.employee_ids

    @api.multi
    def name_get(self):
        """name_get() -> [(id, name), ...]

        Returns a textual representation for the records in ``self``.
        By default this is the value of the ``display_name`` field.

        :return: list of pairs ``(id, text_repr)`` for each records
        :rtype: list(tuple)
        """
        result = []
        for record in self:
            result.append((record.id, _("Jobseekers")))
        return result

    @api.multi
    def search_jobseeker(self):
        if self.identification == False:
            raise ValidationError(_("Identification must be set before searching"))
        elif self.search_reason == "other reason":
            if not self.other_reason:
                raise ValidationError(
                    _("Other reason selected but other reason field is not filled in")
                )
            if len(self.other_reason) < 20:
                raise ValidationError(
                    _("Other reason has to be at least 20 characters long")
                )

        partners = self.env["res.partner"].sudo().search(self.get_domain())
        if not partners:
            # ”Hänvisning till Sök-A/AIS-F, den arbetssökande finns inte i Kundrelationssystemet”
            raise ValidationError(
                _(
                    "Refer to Sök-A/AIS-F, the jobseeker does not exist in the Kundrelationssystem"
                )
            )
        # TODO: Set correct access level. Probably varies with the reason for the search.
        partners._grant_jobseeker_access(
            "MYCKET_STARK",
            user=self.env.user,
            reason=self.search_reason or self.identification,
        )
        for partner in partners:
            vals = {
                "logged_in_user": self.env.user.name,
                "identification": self.identification,
                "searched_partner": partner.name,
                "social_sec_num": partner.social_sec_nr,
                "office": partner.office_id.name,
            }
        action = {
            "name": _("Jobseekers"),
            "domain": [("id", "=", partners._ids), ("is_jobseeker", "=", True)],
            "res_model": "res.partner",
            "context": {"bos_postcode": True},
            "view_ids": [
                self.env.ref("partner_view_360.view_jobseeker_kanban").id,
                self.env.ref("partner_view_360.view_jobseeker_form").id,
                self.env.ref("partner_view_360.view_jobseeker_tree").id,
            ],
            "view_mode": "kanban,tree,form",
            "type": "ir.actions.act_window",
            "target": "main",
        }
        if len(partners) == 1:
            action["view_id"] = self.env.ref("partner_view_360.view_jobseeker_form").id
            action["res_id"] = partners.id
            action["view_mode"] = "form"
        return action

    @api.multi
    def search_jobseeker_authority(self):
        if self.search_reason == False:
            raise ValidationError(_("Search reason must be set before searching"))
        elif self.search_reason == "other reason":
            if not self.other_reason:
                raise ValidationError(
                    _("Other reason selected but other reason field is not filled in")
                )
            if len(self.other_reason) < 20:
                raise ValidationError(
                    _("Other reason has to be at least 20 characters long")
                )

        partners = self.env["res.partner"].sudo().search(self.get_domain())
        if not partners:
            raise ValidationError(
                _(
                    "Refer to Sök-A/AIS-F, the jobseeker does not exist in the Kundrelationssystem"
                )
            )
        # TODO: Set correct access level. Probably varies with the reason for the search.
        partners._grant_jobseeker_access(
            "MYCKET_STARK",
            user=self.env.user,
            reason=self.search_reason or self.identification,
        )
        for partner in partners:
            vals = {
                "logged_in_user": self.env.user.name,
                "identification": self.identification,
                "searched_partner": partner.name,
                "social_sec_num": partner.social_sec_nr,
                "office": partner.office_id.name,
            }

            _logger.info(json.dumps(vals))
        action = {
            "name": _("Jobseekers"),
            "domain": [("id", "=", partners._ids), ("is_jobseeker", "=", True)],
            "context": {"bos_postcode": True},
            "res_model": "res.partner",
            "view_ids": [
                self.env.ref("partner_view_360.view_jobseeker_kanban").id,
                self.env.ref("partner_view_360.view_jobseeker_form").id,
                self.env.ref("partner_view_360.view_jobseeker_tree").id,
            ],
            "view_mode": "kanban,tree,form",
            "type": "ir.actions.act_window",
            "target": "main",
        }
        if len(partners) == 1:
            action["view_id"] = self.env.ref("partner_view_360.view_jobseeker_form").id
            action["res_id"] = partners.id
            action["view_mode"] = "form"

        return action


    @api.multi
    def get_domain(self):
        now_year = str(datetime.now().year)
        last_century = str(int(now_year) - 100)[0:2]
        domain = []
        if self.social_sec_nr_search:
            pnr = self.social_sec_nr_search.strip().replace('-', '')
            if not pnr.isdigit():
                raise Warning(_("Please only enter digit!"))
            if len(pnr) not in (10, 12):
                raise Warning(_("Incorrectly formatted social security number: %s")
                              % self.social_sec_nr_search)
            if len(pnr) == 12:
                if pnr[:2] not in (last_century, now_year[0:2]):
                    raise Warning(_("Invalid year!"))
                pnr = pnr[2:]
            if not validate_personnummer(pnr):
                raise Warning(_("Invalid control number!"))
            if (
                    len(self.social_sec_nr_search) == 13
                    and self.social_sec_nr_search[8] == "-"
            ):
                domain.append(("social_sec_nr", "=", self.social_sec_nr_search))
            elif len(self.social_sec_nr_search) == 12 and "-" not in self.social_sec_nr_search:

                domain.append(
                    (
                        "social_sec_nr",
                        "=",
                        "%s-%s"
                        % (
                            self.social_sec_nr_search[:8],
                            self.social_sec_nr_search[8:12],
                        ),
                    )
                )
            elif (
                    len(self.social_sec_nr_search) == 11
                    and self.social_sec_nr_search[6] == "-"
            ):
                if self.social_sec_nr_search[0:2] < now_year[2:4]:
                    domain.append(("social_sec_nr", "=", now_year[0:2] + self.social_sec_nr_search))
                else:
                    domain.append(("social_sec_nr", "=", last_century + self.social_sec_nr_search))
            elif len(self.social_sec_nr_search) == 10 and "-" not in self.social_sec_nr_search:
                if self.social_sec_nr_search[0:2] < now_year[2:4]:
                    domain.append(
                        (
                            "social_sec_nr",
                            "=",
                            "%s-%s"
                            % (
                                now_year[0:2] + self.social_sec_nr_search[:6],
                                self.social_sec_nr_search[6:10],
                            ),
                        )
                    )
                else:
                    domain.append(
                        (
                            "social_sec_nr",
                            "=",
                            "%s-%s"
                            % (
                                last_century + self.social_sec_nr_search[:6],
                                self.social_sec_nr_search[6:10],
                            ),
                        )
                    )
            else:
                raise ValidationError(
                    _("Incorrectly formatted social security number: %s")
                    % self.social_sec_nr_search
                )
        if self.customer_id_search:
            ipf = self.env.ref("af_ipf.ipf_endpoint_customer").sudo()
            res = ipf.call(customer_id=self.customer_id_search)
            pnr = None
            if res:
                pnr = res.get("ids", {}).get("pnr")
                if pnr:
                    if len(pnr) == 12 and '-' not in pnr:
                        pnr = "%s-%s" % (pnr[:8], pnr[8:12])
                    elif len(pnr) == 10 and '-' not in pnr:
                        if pnr[0:2] < now_year[2:4]:
                            pnr = "%s-%s" % (now_year[0:2] + pnr[:6], pnr[6:10])
                        else:
                            pnr = "%s-%s" % (last_century + pnr[:6], pnr[6:10])
            if pnr:
                domain.append(("social_sec_nr", "=", pnr))
            else:
                domain.append(("social_sec_nr", "in", []))
        if self.email_search:
            domain.append(("email", "=", self.email_search))
        domain = ["|" for x in range(len(domain) - 1)] + domain
        domain.insert(0, ("is_jobseeker", "=", True))
        domain.insert(0, ("is_spu", "=", False))
        return domain

    @api.multi
    def do_bankid(self):
        """Send BankID request and wait for user verification."""
        self.bank_id_ok = False
        if not self.social_sec_nr_search:
            raise ValidationError(_("Social security number missing"))
        ipf_auth = self.env.ref(
            'af_ipf.bankid_endpoint_elegservice_auth').sudo()
        ipf_collect = self.env.ref(
            'af_ipf.bankid_endpoint_elegservice_collect').sudo()
        res = ipf_auth.call(
            body=
            {
                "systemID": "AFCRM",
                "authSystem": "bankid",
                "personalNumber": self.social_sec_nr_search.replace("-", ""),
            }
        )
        order_ref = None
        try:
            order_ref = res["orderRef"]
            if not order_ref:
                self.bank_id_ok = False
                try:
                    self.bank_id_text = res["infoCode"]
                except (KeyError, TypeError):
                    self.bank_id_text = _("Error in communication with BankID")
        except (KeyError, TypeError):
            self.bank_id_text = _("Error in communication with BankID")
            self.bank_id_ok = False
        if order_ref:
            deadline = time.monotonic() + TIMEOUT
            time.sleep(9)  # Give user time to react before polling.
            while deadline > time.monotonic():
                res_collect = ipf_collect.call(body={
                    "systemID": "AFCRM",
                    "orderRef": order_ref
                })
                if "status" in res_collect and \
                        res_collect["status"] == "complete":
                    self.bank_id_text = res_collect["status"]
                    self.bank_id_ok = True
                    break
                elif "status" in res_collect and \
                        res_collect["status"] == "failed":
                    self.bank_id_text = res_collect["infoCode"]
                    self.bank_id_ok = False
                    break
                time.sleep(3)
            else:
                self.bank_id_text = _("User timeout")
                self.bank_id_ok = False

        if not self.bank_id_ok:
            raise ValidationError(self.bank_id_text)

        partner = self.env["res.partner"].search_pnr(
            self.social_sec_nr_search)

        if not partner:
            raise ValidationError(
                _("Social security number not found in system"))
        # create bankid token to let user know status of bankid process
        bankid_vals = {
            "name": self.bank_id_text,
            "user_id": self.env.user.id,
            "partner_id": partner.id,
        }
        request.env["res.partner.bankid"].create(bankid_vals)
        if self.bank_id_ok:
            action = (
                self.env["ir.actions.act_window"]
                    .browse(self.env.ref(
                    "hr_360_view.search_jobseeker_wizard").id)
                    .read()[0]
            )
            action["res_id"] = self.id
            action["view_mode"] = "form"
            return action
