# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution, third party addon
#    Copyright (C) 2020 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import json
import logging
import requests
from odoo.exceptions import Warning
from requests.auth import HTTPBasicAuth
from uuid import uuid4

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class AfIpf(models.Model):
    _name = 'af.ipf'
    _description = 'IPF Integration'

    name = fields.Char(required=True)
    clientid = fields.Char(string='Client Id', help="Found in IPF portal")
    client_secret = fields.Char(string='Client Secret', help="Found in IPF portal")
    auth_user = fields.Char()
    auth_password = fields.Char()
    systemid = fields.Char(default='AFCRM')
    environment = fields.Selection(selection=[
        ('U1', 'U1'),
        ('I1', 'I1'),
        ('T1', 'T1'),
        ('T2', 'T2'),
        ('PROD', 'PROD'),
        ('OTHER', 'OTHER')],
        default='T2',
        required=True)
    enduserid = fields.Boolean()
    enduserid_hardcoded = fields.Boolean()
    endpoint_ids = fields.One2many(comodel_name='af.ipf.endpoint', inverse_name='ipf_id')
    url = fields.Char(string='IPF url', help="AF's web address", default='https://ipfapi.arbetsformedlingen.se',
                      required=True)
    port = fields.Integer(string='IPF port', help="Af's port, default 443", default=443, required=True)
    ssl_verify = fields.Char()
    ssl_cert = fields.Char()
    ssl_key = fields.Char()

    @api.multi
    def get_auth(self):
        self.ensure_one()
        if self.auth_user and self.auth_password:
            return HTTPBasicAuth(self.auth_user, self.auth_password)

    @api.multi
    def get_headers(self):
        self.ensure_one()
        headers = {
            'AF-SystemId': self.systemid,
            'AF-Environment': self.environment,
            'AF-TrackingId': '%s' % uuid4(),
        }
        if self.enduserid:
            if self.enduserid_hardcoded:
                headers['AF-EndUserId'] = '*sys*'
            else:
                user = self._context.get('uid')
                user = user and self.env['res.users'].browse(user) or self.env.user
                headers['AF-EndUserId'] = user.af_signature
        return headers 

    @api.multi
    def get_ssl_params(self):
        ssl_params = {
        }
        if not self.ssl_verify:
            ssl_params['verify'] = False
        else:
            ssl_params['verify'] = self.ssl_verify
        if self.ssl_cert and self.ssl_key:
            ssl_params['cert'] = (ssl_cert, ssl_key)
        return ssl_params


class AfIpfEndpoint(models.Model):
    _name = 'af.ipf.endpoint'
    _description = 'IPF Endpoint'

    name = fields.Char(required=True)
    ipf_id = fields.Many2one(comodel_name='af.ipf', required=True, ondelete='cascade')

    @api.multi
    def build_error_msg(self, response, data):
        """Build error message from JSON response."""
        return "%s: %s [%s] %s" % (self.ipf_id.name, self.name, response.status_code, data)

    @api.multi
    def call(self, raise_on_error=False, **kw):
        self.ensure_one()
        headers = self.ipf_id.get_headers()
        if 'AF-EndUserId' in headers and not headers['AF-EndUserId']:
            # This integration requires a signature, but user doesn't have one.
            return
        kw.update({
            'clientid': self.ipf_id.clientid,
            'client_secret': self.ipf_id.client_secret,
        })
        url = '%s:%s/%s' % (
            self.ipf_id.url,
            self.ipf_id.port,
            self.name.format(**kw))
        _logger.debug("Unpack url: %s" % url)
        response = requests.get(
            url,
            headers=headers,
            auth=self.ipf_id.get_auth(),
            **self.ipf_id.get_ssl_params()
        )
        _logger.debug("Unpack response: %s" % response)
        res = None
        try:
            res = response.json()
        except:
            pass
        if response.status_code != 200:
            error_msg = self.build_error_msg(response, res)
            _logger.warn(error_msg)
            if raise_on_error:
                raise Warning(error_msg)
        # Undocumented response from Customer. No data returned in body.
        # if response.status_code == 204:
        #    return
        _logger.debug("Unpack body: %s" % res)
        return res

    @api.model
    def get_pnr(self, customer_id):
        ipf = self.env.ref('af_ipf.ipf_endpoint_customer')
        res = ipf.call(customer_id = customer_id)
        pnr = res.get('ids', {}).get('pnr')
        if len(pnr) == 12:
            pnr = pnr[:8] + "-" + pnr[8:12]
        return pnr