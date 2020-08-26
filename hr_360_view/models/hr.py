from odoo import models, fields, api, _


class HR(models.Model):
    _inherit = 'hr.employee'

    related_partner_id = fields.Many2one('res.partner', string="Related Partner", related='user_id.partner_id')

    reason_or_id = fields.Selection(string="Access by reason or identification?",
                                    selection=[('reason', 'Reason'), ('id', 'Identification')])
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
    search_domain = fields.Char(string="Search Filter",
                                default='["|","|",("social_sec_nr","=",""),("customer_id","=",""),("email","=","")]')
    other_reason = fields.Char(string="Other reason")

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
    def search_jobseeker(self):
        pass
