# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2019 Vertel AB (<http://vertel.se>).
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

import logging
from suds.client import *  # SOAP pip3 install suds-py3

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class ResPartnerEleg(models.TransientModel):
    _name = 'res.partner.eleg'

    user_id = fields.Many2one(comodel_name="res.users")
    partner_id = fields.Many2one(comodel_name="res.partner")

    def create_eleg(self, partner):
        """
          Creates record for checking eleg, this record will varnish inte some minutes
        """
        self.env['res.partner.eleg'].create({'user_id': self.env.user.id, 'partner_id': partner.id})


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def init_bank_id(self, personnummer):
        bankid = suds.client.Client(
            'http://bhipws.arbetsformedlingen.se/Integrationspunkt/ws/mobiltbankidinterntjanst?wsdl')  # create a Client instance
        res = bankid.MobiltBankIDInternTjanst(personnummer)
        if res:
            pass
