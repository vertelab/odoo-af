# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
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
import logging
_logger = logging.getLogger(__name__)

    
class ResPartner(models.Model):
    _inherit = "res.partner"

    # Access rights to archive contacts. This is probably not good enough.
    # Can't specify read/write.
    # Can't specify domains per group (causes crossover between employers and jobseekers officers)
    # TODO: Look for a solution. Existing module or build one.
    #       Look at that encryption module to add new parameters to fields.
    active = fields.Boolean(groups='base.group_system,af_security.group_af_employers_high,af_security.group_af_jobseekers_high')

    @api.model
    def af_security_install_rules(self):
        self.env.ref('base.res_partner_rule_private_employee').active = False