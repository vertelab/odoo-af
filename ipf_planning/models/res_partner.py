# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
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


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def ipf_load_planning(self):
        self.ensure_one()
        res = None
        if self.is_jobseeker:
            personnummer = self.get_ais_a_pnr()
            if personnummer:
                try:
                    ipf = self.env.ref('af_ipf.ipf_endpoint_planning').sudo()
                    res = ipf.call(personnummer=personnummer)
                except Exception as e:
                    _logger.warn('Error in IPF Planning integration.', exc_info=e)
        return res

    @api.multi
    def get_ais_a_pnr(self):
        try:
            if self.company_registry:
                pnr = self.company_registry.replace('-', '')
                return pnr
        except:
            _logger.warn("Invalid personal identification number: %s" % self.company_registry)
