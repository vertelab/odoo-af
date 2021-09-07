from odoo import models, fields, api, _
from odoo.http import request

import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.multi
    def get_contact_links(self):
        """Generate link json data for this partner. Used by the ContactLinks widget."""
        links = self.env["partner.links"].search(
            [
                "|",
                ("group_ids", "=", False),
                ("group_ids", "in", self.env.user.groups_id.ids),
            ]
        )
        if links:
            return links.get_links(self)


class PartnerLinks(models.Model):
    _name = "partner.links"
    _description = "Partner Links"
    _order = "sequence"

    name = fields.Char("Display Name")
    link = fields.Char(
        "Link",
        help="Supports parameterization through pythons format function.\n"
        "Example: https://example.com/arbetssokande?personnummer={partner.social_sec_nr}&signatur={user.af_signature}\n"
        "format receives the following input:\n"
        "* partner: The current res.partner (Contakt, Job seeker, etc)\n"
        "* user: The logged in user.",
    )
    target = fields.Selection(
        [
            ("blank", "_blank"),
            ("self", "_self"),
            ("parent", "_parent"),
            ("top", "_top"),
        ],
        string="Target",
        default="_blank",
    )
    group_ids = fields.Many2many("res.groups", string="Groups")
    image = fields.Binary(
        string="Image",
        attachment=True,
    )
    type_smart = fields.Selection(
        [("tab", "Tab"), ("smart", "Smart Button")], string="Type", default="tab"
    )
    sequence = fields.Integer(string='Order of links')

    @api.one
    def get_links(self, partner):
        """Generate json data from this link object. Used by the ContactLinks widget.
        :param partner: The partner to generate a link for.
        """
        url = None
        try:
            partner = partner.sudo()
            url = self.link.format(
                partner=partner,
                user=self.env.user,
                ais_pnr=partner.social_sec_nr.replace("-", "")[-10:],
                clean_pnr=partner.social_sec_nr.replace("-", ""),
            )
        except:
            # TODO: Improve error feedback. This is pretty useless since the end users won't see the log.
            # Use traceback to build message and return it in the result.
            # Display the error message in the browser console or something.
            # This way it becomes possible for the end users (such as support staff) to follow up on them.
            _logger.exception(
                _("Could not compute Contact Link %s (id %s).") % (self.name, self.id)
            )
        return {
            "url": url,
            "target": self.target,
            "icon": "/web/content/partner.links/%s/image" % self.id,
            "name": self.name,
        }
