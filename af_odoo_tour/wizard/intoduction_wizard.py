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

from datetime import datetime
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import Warning
from odoo import models, fields, api, _
import logging
from datetime import date
_logger = logging.getLogger(__name__)


class IntroductionWizard(models.Model):
    _name = "introduction.tour.wizard"

    # employee_id = fields.Many2one(comodel_name='hr.employee', default=lambda self: self._default_hr_employee())
    # jobseekers_ids = fields.One2many('res.partner')
    name = fields.Char("Name")
    case_ids = fields.One2many('res.partner.case', 'intoduction_rec_id')
    daily_note_ids = fields.One2many('res.partner.notes', 'intoduction_rec_id')
    upcomming_appoitment_ids = fields.One2many(
        'calendar.appointment', 'intoduction_rec_id')

    # search_reason = fields.Selection(string="Search
    # reason",selection=[('record incoming documents','Record incoming
    # documents'), ("follow-up of job seekers' planning","Follow-up of job
    # seekers' planning"), ('directory Assistance','Directory Assistance'),
    # ('matching','Matching'), ('decisions for other officer','Decisions for
    # other officer'),('administration of recruitment meeting/group
    # activity/project','Administration of recruitment meeting/group
    # activity/project'),('investigation','Investigation'),('callback','Callback'),('other
    # reason','Other reason')])#
    identification = fields.Selection(
        string="Identification",
        selection=[
            ('id document',
             'ID document'),
            ('Digital ID',
             'Digital ID'),
            ('id document-card/residence permit card',
             'ID document-card/Residence permit card'),
            ('known (previously identified)',
             'Known (previously identified)'),
            ('identified by certifier',
             'Identified by certifier')])

    social_sec_nr_search = fields.Char(string="Social security number")
    # customer_id_search = fields.Char(string="Customer number")
    # email_search = fields.Char(string="Email")

    search_domain = fields.Char(string="Search Filter")
    # other_reason = fields.Char(string="Other reason")

    @api.onchange('identification', 'social_sec_nr_search')
    def onchange_sec_no_iden(self):
        self.case_ids = [(6, 0, [])]
        self.daily_note_ids = [(6, 0, [])]
        self.upcomming_appoitment_ids = [(6, 0, [])]

    @api.depends('employee_id')
    def _get_records(self):
        for rec in self:
            if rec.employee_id.user_id:
                rec.jobseekers_ids = rec.env['res.partner'].search(
                    [('user_id', '=', rec.employee_id.user_id.id)])
                rec.case_ids = rec.env['res.partner.case'].search(
                    [('administrative_officer', '=', rec.employee_id.user_id.id)])
                rec.daily_note_ids = rec.env['res.partner.notes'].search(
                    [('administrative_officer', '=', rec.employee_id.user_id.id)])

    # def _default_hr_employee(self):
    #     return self.env.user.employee_ids

    @api.multi
    # def name_get(self):
    #     """ name_get() -> [(id, name), ...]
    #
    #     Returns a textual representation for the records in ``self``.
    #     By default this is the value of the ``display_name`` field.
    #
    #     :return: list of pairs ``(id, text_repr)`` for each records
    #     :rtype: list(tuple)
    #     """
    # result = []
    # for record in self:
    #     result.append((record.id, _('Handläggaryta')))
    # return result
    @api.multi
    def search_jobseeker(self):
        # TODO: This should be made into two separate functions so it's 100%
        # clear what the user is trying to do.
        now_year = str(datetime.now().year)
        last_century = str(int(now_year) - 100)[0:2]
        domain = []
        if self.social_sec_nr_search:
            if len(
                    self.social_sec_nr_search) == 13 and self.social_sec_nr_search[8] == "-":
                domain.append(
                    ("social_sec_nr", "=", self.social_sec_nr_search))
            elif len(self.social_sec_nr_search) == 12 and "-" not in self.social_sec_nr_search:
                domain.append(("social_sec_nr",
                               "=",
                               "%s-%s" % (self.social_sec_nr_search[:8],
                                          self.social_sec_nr_search[8:12])))
            elif len(
                    self.social_sec_nr_search) == 11 and self.social_sec_nr_search[6] == "-":
                if self.social_sec_nr_search[0:2] < now_year[2:4]:
                    domain.append(
                        ("social_sec_nr", "=", now_year[0:2] + self.social_sec_nr_search))
                else:
                    domain.append(
                        ("social_sec_nr", "=", last_century + self.social_sec_nr_search))

            elif len(self.social_sec_nr_search) == 10 and "-" not in self.social_sec_nr_search:
                if self.social_sec_nr_search[0:2] < now_year[2:4]:
                    domain.append(("social_sec_nr",
                                   "=",
                                   "%s-%s" % (now_year[0:2] + self.social_sec_nr_search[:6],
                                              self.social_sec_nr_search[6:10])))
                else:
                    domain.append(("social_sec_nr",
                                   "=",
                                   "%s-%s" % (last_century + self.social_sec_nr_search[:6],
                                              self.social_sec_nr_search[6:10])))
            else:
                raise Warning(
                    _("Incorrectly formated social security number: %s" % self.social_sec_nr_search))
        # if self.customer_id_search:
        #     domain.append(("customer_id", "=", self.customer_id_search))
        # if self.email_search:
        #     domain.append(("email", "=", self.email_search))
        domain = ['|' for x in range(len(domain) - 1)] + domain
        # domain.insert(0, ('is_jobseeker', '=', True))
        _logger.info("domain: %s" % domain)

        # if self.identification == False:
        #     raise Warning(_("Search reason or identification must be set before searching"))
        # elif self.search_reason == "other reason" and self.other_reason == False:
        #     raise Warning(_("Other reason selected but other reason field is not filled in"))

        partners = self.env['res.partner'].sudo().search(domain)
        if not partners:
            raise Warning(_("No id found"))
        # TODO: Set correct access level. Probably varies with the reason for the search.
        # partners._grant_jobseeker_access('MYCKET_STARK', user=self.env.user, reason=self.search_reason or self.identification)

        self.case_ids = [(6, 0, [])]
        self.daily_note_ids = [(6, 0, [])]
        current_user_id = self.env.user.id
        today_date = datetime.today().date()
        for partner in partners:
            for case in partner.case_ids:
                if case.case_type and (
                        case.case_type.name == 'AIS-Å' or case.case_type.name == 'BÄR'):
                    self.case_ids = [(4, case.id)]
            for note in partner.notes_ids:
                if (note.create_uid.id == current_user_id or note.create_uid.id ==
                        1) and note.create_date.date() == today_date:
                    self.daily_note_ids = [(4, note.id)]
            if partner.appointment_ids:
                upcoming_meetings = partner.appointment_ids.filtered(
                    lambda a: a.start > datetime.now())
                for metting in upcoming_meetings:
                    self.upcomming_appoitment_ids = [(4, metting.id)]

        # action = {
        #     'name': _('Jobseekers'),
        #     'domain': [('id', '=', partners._ids), ('is_jobseeker', '=', True)],
        #     #'view_type': 'tree',
        #     'res_model': 'res.partner',
        #     'view_ids':  [self.env.ref("partner_view_360.view_jobseeker_kanban").id, self.env.ref("partner_view_360.view_jobseeker_form").id, self.env.ref("partner_view_360.view_jobseeker_tree").id],
        #     'view_mode': 'kanban,tree,form',
        #     'type': 'ir.actions.act_window',
        # }
        # if len(partners) == 1:
        #     action['view_id'] = self.env.ref("partner_view_360.view_jobseeker_form").id
        #     action['res_id'] = partners.id
        #     action['view_mode'] = 'form'
        # return action


class ResPartnerCase(models.Model):
    _inherit = "res.partner.case"

    intoduction_rec_id = fields.Many2one('introduction.tour.wizard')


class ResPartnerNotes(models.Model):
    _inherit = "res.partner.notes"

    intoduction_rec_id = fields.Many2one('introduction.tour.wizard')


class CalendarAppointment(models.Model):
    _inherit = 'calendar.appointment'

    intoduction_rec_id = fields.Many2one('introduction.tour.wizard')
