from odoo import models, fields, api, _

class ResPartner(models.Model):

    _inherit = 'res.partner'

    link_ids = fields.One2many('partner.links', 'partner_id', string="Links")


class PartnerLinks(models.Model):

    _name = 'partner.links'
    _description = "Partner Links"

    partner_id = fields.Many2one('res.partner', string="Contact")
    name = fields.Char("Display Name")
    static_url_1 = fields.Char("Static URL Part 1")
    static_url_2 = fields.Char("Static URL Part 2")
    inserted_field = fields.Many2one('ir.model.fields', string="Inserted Field")
    target = fields.Selection([('blank', '_blank'),
                               ('self', '_self'),
                               ('parent', '_parent'),
                               ('top', '_top')], string="Target")
    group_ids = fields.Many2many('res.groups', string="Groups")
    link = fields.Char("Link")

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        args = args or []
        if not self.env.user.has_group('contact_links.group_partner_link'):
            args += [('group_ids', 'in', self.env.user.groups_id.ids)]
        res = super(PartnerLinks, self).search(args=args, offset=offset, limit=limit, order=order,
                                               count=count)
        return res

    @api.onchange('static_url_1', 'static_url_2')
    def onchange_static_url(self):
        if self.static_url_1 or self.static_url_2:
            link = ''
            link += self.static_url_1 if self.static_url_1 else ''
            if self.static_url_1 and self.static_url_2:
                link += '...'
            link += self.static_url_2 if self.static_url_2 else ''
            self.link = link