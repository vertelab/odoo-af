from odoo import models, fields, api, _

class UpdateDashboardConfiguration(models.TransientModel):

    _name = 'update.dashboard.config'
    _description = "Update Dashboard"

    welcome_msg = fields.Char("Welcome String")
    welcome_dsc = fields.Html("Welcome Description")
    want_to_update_welcome_data = fields.Boolean("Want to update Welcome Data?")
    name = fields.Html("Title")
    sub_title = fields.Html("Sub title")
    description = fields.Html("Description")
    image = fields.Char("Image Class")
    group_ids = fields.Many2many("res.groups", "rel_update_dashboax_box_group", "update_dash__id",
                                 "rel_update_dah_group_id", "Groups")
    action_id = fields.Many2one("ir.actions.act_window", "Action")
    action_url = fields.Char("Action URL", compute="_compute_action_url")
    user_ids = fields.Many2many("res.users", "rel_update_dah_users", "user_id", "rel_dash_user_id")

    def add_boxes(self):
        config_obj = self.env['af.dashboard']
        for user in self.user_ids:
            config = config_obj.search([('user_id', '=', user.id)], limit=1)
            if config:
                if self.want_to_update_welcome_data:
                    config.welcome_msg = self.welcome_msg
                    config.welcome_dsc = self.welcome_dsc
                if self.image or self.group_ids or self.action_id:
                    config.box_ids = [(0, 0, {
                        'name': self.name,
                        'sub_title': self.sub_title,
                        'description': self.description,
                        'image': self.image,
                        'group_ids': [(4, group.id) for group in self.group_ids],
                        # 'is_group': self.is_group,
                        'action_id': self.action_id if self.action_id.id else False,
                        'action_url': self.action_url
                    })]

    @api.depends('action_id')
    def _compute_action_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for box in self:
            if box.action_id:
                link = '%s/web#action=%s&model=%s' % (base_url, box.action_id.id, box.action_id.res_model)
                box.action_url = link

    # @api.depends('group_ids', 'af_dashboard_id.user_id.groups_id')
    # def _compare_box_user_group(self):
    #     for box in self:
    #         is_group = False
    #         if box.group_ids and box.af_dashboard_id and box.af_dashboard_id.user_id and \
    #                 box.af_dashboard_id.user_id.groups_id:
    #             for group in box.group_ids:
    #                 if not is_group and group.id in box.af_dashboard_id.user_id.groups_id.ids:
    #                     is_group = True
    #                     box.is_group = True
    #                 else:
    #                     is_group = False
    #
    #
