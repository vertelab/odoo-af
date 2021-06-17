from odoo import models, fields, api, _


@api.model
def _lang_get(self):
    return self.env['res.lang'].get_installed()


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    lang = fields.Selection(_lang_get, related='partner_id.lang', store=True, string="Client's Language")
    employee_id = fields.Many2one('hr.employee', string="Employee")
    skill_ids = fields.One2many('hr.employee.skill.sale', 'sale_order_id', string="Employee skills",
                                compute='_get_employee_skills', store=True)

    def update_employee(self):
        emp_obj = self.env['hr.employee']
        for rec in self:
            if rec.user_id:
                employee = emp_obj.search([('user_id', '=', rec.user_id.id)], limit=1)
                if employee:
                    rec.employee_id = employee.id

    @api.onchange('user_id')
    def onchange_user_id(self):
        if self.user_id:
            employee = self.env['hr.employee'].search([('user_id', '=', self.user_id.id)], limit=1)
            if employee:
                self.employee_id = employee.id

    @api.depends('employee_id', 'employee_id.employee_skill_ids')
    def _get_employee_skills(self):
        for rec in self:
            if rec.employee_id and rec.employee_id.employee_skill_ids:
                if rec.skill_ids:
                    rec.skill_ids = [(5, 0)]
                for skill in rec.employee_id.employee_skill_ids:
                    rec.skill_ids = [(0, 0, {
                        'employee_id': skill.employee_id.id if skill.employee_id else False,
                        'skill_id': skill.skill_id.id if skill.skill_id else False,
                        'level': skill.level,
                    })]


class HRSkill(models.Model):
    _name = 'hr.employee.skill.sale'
    _description = "HR Employee Skill Sale"

    sale_order_id = fields.Many2one('sale.order')
    employee_id = fields.Many2one(
        string='Employee',
        comodel_name='hr.employee',
    )
    skill_id = fields.Many2one(
        string='Skill',
        comodel_name='hr.skill',
    )
    level = fields.Selection(
        string='Level',
        selection=[
            ('0', 'Junior'),
            ('1', 'Intermediate'),
            ('2', 'Senior'),
            ('3', 'Expert'),
        ],
    )
