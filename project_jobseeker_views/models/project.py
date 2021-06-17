from datetime import datetime

from odoo import models, fields, api, _


class ProjectProject(models.Model):
    _inherit = 'project.project'

    case_number = fields.Char(related='sale_order_id.client_order_ref', string="Case Number")
    service = fields.Many2one(related='sale_line_id.product_id', string="Service")
    project_next_task = fields.Many2one('project.task', string="Next Task", compute='_update_fields')
    project_next_task_due_date = fields.Date(related='project_next_task.date_deadline', string="Next Task Due Date")
    task_new_event = fields.Char(string="Task New Event", compute='_get_mail_activity')

    @api.depends('sale_order_id')
    def _update_fields(self):
        for rec in self:
            if rec.sale_order_id and (rec.task_count > 0):
                for _ in rec.tasks:
                    if (_.date_start.date() <= datetime.today().date()) and (_.stage_id.name != 'Done'):
                        rec.project_next_task = rec.tasks[0]

    @api.depends('project_next_task')
    def _get_mail_activity(self):
        for rec in self:
            if rec.project_next_task:
                activity_ids = rec.env['mail.activity'].search([
                    ('res_model', '=', 'project.task'), ('res_id', '=', rec.project_next_task.id)
                ], limit=1, order="id desc")
                if activity_ids:
                    rec.task_new_event = activity_ids.activity_type_id.name
