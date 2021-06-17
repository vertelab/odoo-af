from odoo import models, fields, api, _


class Dashboard(models.Model):
    _name = 'af.dashboard'
    _description = "AF Dashboard"

    name = fields.Char("Name")
    user_id = fields.Many2one('res.users', "User")
    # task_ids = fields.One2many('project.task', 'af_dashboard_id', compute="get_tasks")

    # def get_tasks(self):
    #     for rec in self:
    #         if rec.user_id:
    #             tasks = self.env['project.task'].sudo().search([('user_id', '=', rec.user_id.id)]).ids
    #             print ("Tasks =-=", tasks)
    #             if tasks:
    #                 rec.task_ids = [(4, task) for task in tasks]
    #                 print ("dfdsfdsgsdg", rec.task_ids)


class ProjectTask(models.Model):
    _inherit = 'project.task'

    af_dashboard_id = fields.Many2one('af.dashboard')


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        res = super(ResUsers, self).create(vals)
        if res:
            self.env['af.dashboard'].sudo().create({
                'name': res.name,
                'user_id': res.id
            })
        return res
