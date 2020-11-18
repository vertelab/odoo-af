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

from datetime import date
import json
import logging
import time
from zeep.client import CachingClient


from odoo import models, fields, api, _
from odoo.exceptions import Warning
from odoo.tools.safe_eval import safe_eval
from odoo.http import request

_logger = logging.getLogger(__name__)
TIMEOUT = 60 * 3

class HrEmployeeJobseekerSearchWizard(models.TransientModel):
    _name = "hr.employee.jobseeker.search.wizard"

    @api.model
    def _get_default_social_sec_nr_search(self):
        ssn_not_found = request.session.pop('ssn_not_found',False)
        if ssn_not_found:
            raise Warning(_("This jobseeker is not registered at Arbetsförmedlingen"))
        return request.session.pop('ssn','')

    # gdpr_id = fields.Many2one('gdpr.inventory')
    # gdpr_reasons = fields.Many2one(related="gdpr_id.reasons?")
    employee_id = fields.Many2one(comodel_name='hr.employee', default=lambda self: self._default_hr_employee())
    jobseekers_ids = fields.One2many('res.partner', compute='_get_records')
    # case_ids = fields.One2many('res.partner.case', compute='_get_records')
    daily_note_ids = fields.One2many('res.partner.notes', compute='_get_records')
    # Looks like related doesn't work on computed fields :(
    # jobseekers_ids = fields.One2many(related='employee_id.jobseekers_ids')
    # case_ids = fields.One2many(related='employee_id.case_ids')
    # daily_note_ids = fields.One2many(related='employee_id.daily_note_ids')
    social_sec_nr_search = fields.Char(string="Social security number",default=lambda self: '%s' % self._get_default_social_sec_nr_search())
    bank_id_text = fields.Text(string=None)
    bank_id_ok = fields.Boolean(string=None,default=False)

    search_reason = fields.Selection(string="Search reason",
                                     selection=[('record incoming documents', 'Record incoming documents'), (
                                     "follow-up of job seekers' planning", "Follow-up of job seekers' planning"),
                                                ('directory Assistance', 'Directory Assistance'),
                                                ('matching', 'Matching'),
                                                ('decisions for other officer', 'Decisions for other officer'), (
                                                'administration of recruitment meeting/group activity/project',
                                                'Administration of recruitment meeting/group activity/project'),
                                                ('investigation', 'Investigation'), ('callback', 'Callback'),
                                                ('other reason', 'Other reason')])  #
    identification = fields.Selection(string="Identification",
                                      selection=[('id document', 'ID document'), ('Digital ID', 'Digital ID'), (
                                      'id document-card/residence permit card',
                                      'ID document-card/Residence permit card'),
                                                 ('known (previously identified)', 'Known (previously identified)'),
                                                 ('identified by certifier', 'Identified by certifier')])  #

    customer_id_search = fields.Char(string="Customer number")
    email_search = fields.Char(string="Email")

    search_domain = fields.Char(string="Search Filter")
    other_reason = fields.Char(string="Other reason")

    @api.depends('employee_id')
    def _get_records(self):
        for rec in self:
            if rec.employee_id.user_id:
                rec.jobseekers_ids = rec.env['res.partner'].search([('user_id', '=', rec.employee_id.user_id.id)])
                # rec.case_ids = rec.env['res.partner.case'].search([('administrative_officer', '=', rec.employee_id.user_id.id)])
                rec.daily_note_ids = rec.env['res.partner.notes'].search(
                    [('administrative_officer', '=', rec.employee_id.user_id.id)])

    def _default_hr_employee(self):
        return self.env.user.employee_ids

    @api.multi
    def name_get(self):
        """ name_get() -> [(id, name), ...]

        Returns a textual representation for the records in ``self``.
        By default this is the value of the ``display_name`` field.

        :return: list of pairs ``(id, text_repr)`` for each records
        :rtype: list(tuple)
        """
        result = []
        for record in self:
            result.append((record.id, _('Jobseekers')))
        return result

    @api.multi
    def search_jobseeker(self):
        # TODO: This should be made into two separate functions so it's 100% clear what the user is trying to do.
        domain = []
        if self.social_sec_nr_search:
            if len(self.social_sec_nr_search) == 13 and self.social_sec_nr_search[8] == "-":
                domain.append(("social_sec_nr", "=", self.social_sec_nr_search))
            elif len(self.social_sec_nr_search) == 12:
                domain.append(
                    ("social_sec_nr", "=", "%s-%s" % (self.social_sec_nr_search[:8], self.social_sec_nr_search[8:12])))
            else:
                raise Warning(_("Incorrectly formated social security number: %s" % self.social_sec_nr_search))
        if self.customer_id_search:
            domain.append(("customer_id", "=", self.customer_id_search))
        if self.email_search:
            domain.append(("email", "=", self.email_search))
        domain = ['|' for x in range(len(domain) - 1)] + domain
        domain.insert(0, ('is_jobseeker', '=', True))
        _logger.info("domain: %s" % domain)

        if self.identification == False:
            raise Warning(_("Identification must be set before searching"))
        elif self.search_reason == "other reason" and self.other_reason == False:
            raise Warning(_("Other reason selected but other reason field is not filled in"))

        partners = self.env['res.partner'].sudo().search(domain)
        if not partners:
            raise Warning(_("No id found"))
        # TODO: Set correct access level. Probably varies with the reason for the search.
        partners._grant_jobseeker_access('MYCKET_STARK', user=self.env.user,
                                         reason=self.search_reason or self.identification)

        for partner in partners:
            vals = {
                'logged_in_user': self.env.user.name,
                'identification': self.identification,
                'searched_partner': partner.name,
                'social_sec_num': partner.social_sec_nr,
                'office': partner.office_id.name

            }

            _logger.info(json.dumps(vals))

        action = {
            'name': _('Jobseekers'),
            'domain': [('id', '=', partners._ids), ('is_jobseeker', '=', True)],
            # 'view_type': 'tree',
            'res_model': 'res.partner',
            'view_ids': [self.env.ref("partner_view_360.view_jobseeker_kanban").id,
                         self.env.ref("partner_view_360.view_jobseeker_form").id,
                         self.env.ref("partner_view_360.view_jobseeker_tree").id],
            'view_mode': 'kanban,tree,form',
            'type': 'ir.actions.act_window',
            'target': 'main'
        }
        if len(partners) == 1:
            action['view_id'] = self.env.ref("partner_view_360.view_jobseeker_form").id
            action['res_id'] = partners.id
            action['view_mode'] = 'form'
        return action

    @api.multi
    def search_jobseeker1(self):
        # TODO: This should be made into two separate functions so it's 100% clear what the user is trying to do.
        domain = []
        if self.social_sec_nr_search:
            if len(self.social_sec_nr_search) == 13 and self.social_sec_nr_search[8] == "-":
                domain.append(("social_sec_nr", "=", self.social_sec_nr_search))
            elif len(self.social_sec_nr_search) == 12:
                domain.append(
                    ("social_sec_nr", "=", "%s-%s" % (self.social_sec_nr_search[:8], self.social_sec_nr_search[8:12])))
            else:
                raise Warning(_("Incorrectly formated social security number: %s" % self.social_sec_nr_search))
        if self.customer_id_search:
            ipf = self.env.ref('af_ipf.ipf_endpoint_customer').sudo()
            res = ipf.call(customer_id=self.customer_id_search)
            pnr = None
            if res:
                pnr = res.get('ids', {}).get('pnr')
                if pnr:
                    pnr = '%s-%s' % (pnr[:8], pnr[8:12])
            if pnr:
                domain.append(("social_sec_nr", "=", pnr))
            else:
                domain.append(("social_sec_nr", 'in', []))
        if self.email_search:
            domain.append(("email", "=", self.email_search))
        domain = ['|' for x in range(len(domain) - 1)] + domain
        domain.insert(0, ('is_jobseeker', '=', True))
        _logger.info("domain: %s" % domain)

        if self.search_reason == False:
            raise Warning(_("Search reason must be set before searching"))
        elif self.search_reason == "other reason" and self.other_reason == False:
            raise Warning(_("Other reason selected but other reason field is not filled in"))

        partners = self.env['res.partner'].sudo().search(domain)
        if not partners:
            raise Warning(_("No id found"))
        # TODO: Set correct access level. Probably varies with the reason for the search.
        partners._grant_jobseeker_access('MYCKET_STARK', user=self.env.user,
                                         reason=self.search_reason or self.identification)

        for partner in partners:
            vals = {
                'logged_in_user': self.env.user.name,
                'identification': self.identification,
                'searched_partner': partner.name,
                'social_sec_num': partner.social_sec_nr,
                'office': partner.office_id.name

            }

            _logger.info(json.dumps(vals))

        action = {
            'name': _('Jobseekers'),
            'domain': [('id', '=', partners._ids), ('is_jobseeker', '=', True)],
            # 'view_type': 'tree',
            'res_model': 'res.partner',
            'view_ids': [self.env.ref("partner_view_360.view_jobseeker_kanban").id,
                         self.env.ref("partner_view_360.view_jobseeker_form").id,
                         self.env.ref("partner_view_360.view_jobseeker_tree").id],
            'view_mode': 'kanban,tree,form',
            'type': 'ir.actions.act_window',
            'target': 'main'
        }
        if len(partners) == 1:
            action['view_id'] = self.env.ref("partner_view_360.view_jobseeker_form").id
            action['res_id'] = partners.id
            action['view_mode'] = 'form'

        return action

    @api.multi
    def do_bankid(self):
        """Send BankID request and wait for user verification."""
        self.bank_id_ok = False
        bankid = CachingClient(
            self.env['ir.config_parameter'].sudo().get_param('hr_360_view.bankid_wsdl',
            'http://bhipws.arbetsformedlingen.se/Integrationspunkt/ws/mobiltbankidinterntjanst?wsdl')) # create a Client instance
        if not self.social_sec_nr_search:
           raise Warning(_('Social security number missing'))
        res = bankid.service.startaIdentifiering(
            self.social_sec_nr_search.replace('-',''),
            'crm')
        _logger.warn("res: %s" % res)
        try:
            orderRef = res['orderRef']
            if not orderRef:
                self.bank_id_ok = False
                try:
                    self.bank_id_text = res['felStatusKod']
                except KeyError:
                    self.bank_id_text = _("Error in communication with BankID")
        except KeyError:
            self.bank_id_text = _("Error in communication with BankID")
            self.bank_id_ok = False			
        if orderRef:
            deadline = time.monotonic() + TIMEOUT
            time.sleep(9) # Give user time to react before polling.
            while deadline > time.monotonic():
                res = bankid.service.verifieraIdentifiering(orderRef,'crm')
                _logger.warn("res: %s" % res)
                if 'statusText' in res and res['statusText'] == 'OK':
                    self.bank_id_text = res['statusText']
                    self.bank_id_ok = True
                    break
                elif 'felStatusKod' in res and self.bank_id_text['felStatusKod']:
                    self.bank_id_text = res['felStatusKod']
                    self.bank_id_ok = False
                    break
                time.sleep(3)
            else:
                self.bank_id_text = _("User timeout")
                self.bank_id_ok   = False

        action = self.env['ir.actions.act_window'].browse(self.env.ref('hr_360_view.search_jobseeker_wizard').id).read()[0]
        action['res_id'] = self.id
        action['view_mode'] = 'form'
        return action

