from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):

    _inherit = 'res.partner'

    link_ids = fields.Many2many(
        'partner.links', 'parnter_link_rel', 'partner_id', 'link_id', string="Links")

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

    def sync_link(self):
        for partner in self.env['res.partner'].search([]):
            _logger.info("got this far")
            partner.write({'link_ids': [(5,)]})
            links = self.env['partner.links'].search(
                [('type_smart', '=', 'tab')])
            for link in links:
                _logger.info("got further")
                partner.link_ids =  [(4, link.id)]
            _logger.info("got to the end")


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
