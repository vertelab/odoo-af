from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    link_ids = fields.Many2many(
        'partner.links', 'parnter_link_rel', 'partner_id', 'link_id', string="Links", compute='sync_link')

    link_target_ids = fields.Many2many('partner.links.target', 'parnter_links_target_rel',
                                       'partner_id', string="Target Links", compute='sync_link')

    def action_partner_link(self):
        kanban_view_id = self.env.ref(
            'contact_links.view_partner_links_kanban').ids
        links = self.env['partner.links'].search(
            [('type_smart', '=', 'smart')])
        return {
            'name': self.name,
            'view_mode': 'kanban',
            'views': [[kanban_view_id, 'kanban']],
            'res_model': 'partner.links',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('id', 'in', links.ids)],
        }

    @api.depends('name')
    def sync_link(self):
        for partner in self:
            # partner.write({'link_ids': [(5,)]})
            partner.write({'link_target_ids': [(5,)]})
            links = self.env['partner.links'].search(
                [('type_smart', '=', 'tab')])
            for link in links:
                # partner.link_ids = [(4, link.id)]
                # partner.link_target_ids = [(4, link.id)]

                # Creates Recording After Searching
                link_target_id = partner.env['partner.links.target']
                search_link_target = link_target_id.search([('link_id', '=', link.id), ('partner_id', '=', partner.id)])
                if search_link_target:
                    partner.link_target_ids = [(4, search_link_target.id)]
                else:
                    create_link_target_id = link_target_id.create({
                        'link_id': link.id,
                        'inserted_field': partner.customer_id,
                        'partner_id': partner.id
                    })
                    partner.link_target_ids = [(4, create_link_target_id.id)]


class PartnerLinks(models.Model):
    _name = 'partner.links'
    _description = "Partner Links"

    partner_id = fields.Many2one('res.partner', string="Contact")
    name = fields.Char("Display Name")
    static_url_1 = fields.Char("Static URL Part 1")
    static_url_2 = fields.Char("Static URL Part 2")
    inserted_field = fields.Char(string="Inserted Field")
    target = fields.Selection([('blank', '_blank'),
                               ('self', '_self'),
                               ('parent', '_parent'),
                               ('top', '_top')], string="Target")
    group_ids = fields.Many2many('res.groups', string="Groups")
    link = fields.Char("Link", compute='_compute_link', store=True)
    image = fields.Binary(
        string='Image',
        attachment=True,
    )
    type_smart = fields.Selection([('tab', 'Tab'),
                                   ('smart', 'Smart Button')], string="Type", default='tab')

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        args = args or []
        if not self.env.user.has_group('contact_links.group_partner_link'):
            args += [('group_ids', 'in', self.env.user.groups_id.ids)]
        res = super(PartnerLinks, self).search(args=args, offset=offset, limit=limit, order=order,
                                               count=count)
        return res

    @api.depends('static_url_1', 'inserted_field', 'static_url_2')
    def _compute_link(self):
        for partner in self:
            partner_link = ''
            partner_link += partner.static_url_1 and partner.static_url_1 or ''
            if partner.inserted_field:
                partner_link += "/"
            partner_link += partner.inserted_field and partner.inserted_field or ''
            if partner.static_url_2:
                partner_link += "/"
            partner_link += partner.static_url_2 and partner.static_url_2 or ''
            partner.link = partner_link


class PartnerLinksTarget(models.Model):
    _name = 'partner.links.target'

    link_id = fields.Many2one('partner.links', string="Link")
    partner_id = fields.Many2one('res.partner', string="Contact")
    name = fields.Char(related='link_id.name', string="Name")
    inserted_field = fields.Char(string="Inserted Field")
    link = fields.Char("Link", compute='_compute_link', store=True)

    static_url_1 = fields.Char("Static URL Part 1", related='link_id.static_url_1',)
    static_url_2 = fields.Char("Static URL Part 2", related='link_id.static_url_2',)
    target = fields.Selection([('blank', '_blank'),
                               ('self', '_self'),
                               ('parent', '_parent'),
                               ('top', '_top')], string="Target", related='link_id.target',)
    group_ids = fields.Many2many('res.groups', string="Groups", related='link_id.group_ids',)
    image = fields.Binary(
        string='Image',
        attachment=True,
        related='link_id.image',
    )
    type_smart = fields.Selection([('tab', 'Tab'),
                                   ('smart', 'Smart Button')], string="Type", default='tab',
                                  related='link_id.type_smart',)

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        args = args or []
        if not self.env.user.has_group('contact_links.group_partner_link'):
            args += [('group_ids', 'in', self.env.user.groups_id.ids)]
        res = super(PartnerLinksTarget, self).search(args=args, offset=offset, limit=limit, order=order,
                                               count=count)
        return res

    @api.depends('link_id.static_url_1', 'inserted_field', 'link_id.static_url_2')
    def _compute_link(self):
        for partner in self:
            partner_link = ''
            partner_link += partner.static_url_1 and partner.static_url_1 or ''
            if partner.inserted_field:
                partner_link += "/"
            partner_link += partner.inserted_field and partner.inserted_field or ''
            if partner.static_url_2:
                partner_link += "/"
            partner_link += partner.static_url_2 and partner.static_url_2 or ''
            partner.link = partner_link
