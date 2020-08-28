from odoo import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    partner_id = fields.Many2one(related="user_id.partner_id")
    link_ids = fields.Many2many(related="partner_id.link_ids")

class HrEmployeeJobseekerSearchWizard(models.TransientModel):
    _inherit = "hr.employee.jobseeker.search.wizard"

    link_ids = fields.Many2many(related="employee_id.link_ids")