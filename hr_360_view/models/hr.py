from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class HR(models.Model):
    _inherit = 'hr.employee'

    related_partner_id = fields.Many2one('res.partner', string="Related Partner", related='user_id.partner_id')
    jobseekers_ids = fields.One2many('res.partner', compute='_get_records')
    case_ids = fields.One2many('res.partner.case', compute='_get_records')
    daily_note_ids = fields.One2many('res.partner.notes', compute='_get_records')

    @api.depends('user_id')
    def _get_records(self):
        for rec in self:
            if rec.user_id:
                rec.jobseekers_ids = rec.env['res.partner'].search([('user_id', '=', rec.user_id.id)])
                rec.case_ids = rec.env['res.partner.case'].search([('administrative_officer', '=', rec.user_id.id)])
                rec.daily_note_ids = rec.env['res.partner.notes'].search([('administrative_officer', '=', rec.user_id.id)])

    @api.multi
    def search_jobseeker_action(self):
        return {
            'res_model': 'hr.employee',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('hr_360_view.search_jobseeker_form').id,
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {},
        }
