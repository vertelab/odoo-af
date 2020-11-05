from odoo import models, fields, api, _

class Dashboard(models.Model):

    _name = 'af.dashboard'
    _description = "AF Dashboard"

    name = fields.Char("Name")
    user_id = fields.Many2one('res.users', "User")
    welcome_msg = fields.Char("Welcome String", default="Welcome")
    welcome_dsc = fields.Html("Welcome Description", default=" You will soon be able to visualise and perform "
                    "all your daily tasks as a FA here. You can already create accounts and handle different "
                    "permission rules to your employees under the tab Administration in the menu bar.")
    box_ids = fields.One2many('dashboard.boxes', 'af_dashboard_id')

class DashboardBoxes(models.Model):

    _name = 'dashboard.boxes'
    _description = "Dashboard Boxes"

    af_dashboard_id = fields.Many2one('af.dashboard')
    user_id = fields.Many2one('res.users', related='af_dashboard_id.user_id', store=True)
    name = fields.Html("Title")
    sub_title = fields.Html("Sub title")
    description = fields.Html("Description")
    image = fields.Char("Image Class")
    group_ids = fields.Many2many("res.groups", "rel_dashboax_box_group", "box_id", "rel_box_group_id", "Groups")
    is_group = fields.Boolean("Is Group", compute="_compare_box_user_group")
    action_id = fields.Many2one("ir.actions.act_window", "Action")
    action_url = fields.Char("Action URL", compute="_compute_action_url")

    @api.depends('action_id')
    def _compute_action_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for box in self:
            if box.action_id:
                link = '%s/web#action=%s&model=%s' % (base_url, box.action_id.id, box.action_id.res_model)
                box.action_url = link

    @api.depends('group_ids', 'af_dashboard_id.user_id.groups_id')
    def _compare_box_user_group(self):
        for box in self:
            is_group = False
            if box.group_ids and box.af_dashboard_id and box.af_dashboard_id.user_id and \
                    box.af_dashboard_id.user_id.groups_id:
                for group in box.group_ids:
                    if not is_group and group.id in box.af_dashboard_id.user_id.groups_id.ids:
                        is_group = True
                        box.is_group = True
                    else:
                        is_group = False



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