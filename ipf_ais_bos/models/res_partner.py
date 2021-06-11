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
from datetime import datetime
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = 'res.partner'

    match_area = fields.Selection(
        selection=[
            ("Krom", "Ja - ej ESF"),
            ("KromEsf", "Ja - ESF"),
            ("EjKrom", "Nej"),
        ],
        string="Rusta och matcha-område",
        compute="_get_match_area"
    )

    @api.multi
    def _get_match_area(self):
        """context added in hr_employee_search_wizard.py action. Gets postcode when opened in Arbetsyta wizard """
        if not self.env.context.get("bos_postcode"):
            return
        if self.is_jobseeker:
            postnummer = self.get_postcode()
            if postnummer:
                try:
                    ipf = self.env.ref('ipf_ais_bos.ipf_endpoint_bos').sudo()
                    res = ipf.call(postnummer=postnummer)
                    match_area = res.get("kromTyp")
                    self.match_area = match_area
                except Exception as e:
                    _logger.warning('Error in IPF CASE integration.', exc_info=e)

    @api.multi
    def get_postcode(self):
        try:
            given_address = self.child_ids.filtered(lambda r: r.type == "given address")
            if given_address:
                postcode = given_address[0].zip
                return postcode
        except ValueError:
            raise UserError("Invalid postcode: %s" % given_address)
