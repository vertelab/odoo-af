from odoo import models, fields, api, _


class HR(models.Model):
    _inherit = 'hr.employee'

    related_partner_id = fields.Many2one('res.partner', string="Related Partner", related='user_id.partner_id')
    
    jobseekers_ids = fields.One2many('res.partner', inverse_name="office", compute='_get_records')
    case_ids = fields.One2many('res.partner.case', inverse_name="partner_id", compute='_get_records')
    daily_note_ids = fields.One2many('res.partner.notes', inverse_name="partner_id", compute='_get_records')

    @api.depends('user_id')
    def _get_records(self):
        for rec in self:
            res_partners_record = rec.env['res.partner'].search([('user_id', '=', self.env.uid)])
            rec.jobseekers_ids = res_partners_record

            case_id_record = rec.env['res.partner.case'].search([('administrative_officer', '=', self.env.uid)])
            rec.case_ids = case_id_record

            daily_note_record = rec.env['res.partner.notes'].search([('administrative_officer', '=', self.env.uid)])
            rec.daily_note_ids = daily_note_record

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
