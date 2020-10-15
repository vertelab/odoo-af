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
from odoo import models, fields, api, _
from odoo.exceptions import Warning
import requests
from requests.auth import HTTPBasicAuth
import json
from uuid import uuid4

import logging
_logger = logging.getLogger(__name__)

class AfIpf(models.Model):
    _name = 'af.ipf'
    _description = 'IPF Integration'

    name = fields.Char(required=True)
    clientid = fields.Char()
    client_secret = fields.Char()
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
    endpoint_ids = fields.One2many(comodel_name='af.ipf.endpoint', inverse_name='ipf_id')
    url = fields.Char(default='https://ipfapi.arbetsformedlingen.se', required=True)
    port = fields.Integer(default=443, required=True)
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
    def call(self, **kw):
        kw.update({
            'clientid': self.ipf_id.clientid,
            'client_secret': self.ipf_id.client_secret,
        })
        self.ensure_one()
        url = '%s:%s/%s' % (
            self.ipf_id.url,
            self.ipf_id.port,
            self.name.format(**kw))
        response = requests.get(
            url,
            headers=self.ipf_id.get_headers(),
            auth=self.ipf_id.get_auth(),
            **self.ipf_id.get_ssl_params()
        )
        if response.status_code == 204:
            return
        return response.json()

    @api.model
    def get_pnr(self, customer_id):
        ipf = self.env.ref('af_ipf.ipf_endpoint_customer')
        res = ipf.call(customer_id = customer_id)
        pnr = res.get('ids', {}).get('pnr')
        return pnr