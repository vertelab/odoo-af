# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.exceptions import AccessError, MissingError
from odoo.http import request


class PortalAccount(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(PortalAccount, self)._prepare_portal_layout_values()
        contact_count = request.env['res.partner'].search_count([])
        values['contact_count'] = contact_count
        return values

    @http.route(['/contacts', '/contacts/<int:page>'], type='http', auth="user", website=True)
    def portal_contacts(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        contacts_ids = request.env['res.partner'].sudo().search([])
        values = self._prepare_portal_layout_values()

        values.update({
            'partners': contacts_ids
        })

        return request.render("af_impaired_portal_ui.portal_all_contact_access", values)

    @http.route(['/contact/<int:contact_id>'], type='http', auth="public", website=True)
    def portal_contact_page(self, contact_id, report_type=None, access_token=None, message=False, download=False, **kw):
        contact_obj = request.env['res.partner'].sudo().search([('id', '=', contact_id)])
        values = {
            'contact_info': contact_obj
        }

        return request.render("af_impaired_portal_ui.access_contact_portal_template", values)
