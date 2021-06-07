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
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = 'res.partner'

    has_ipf_planning = fields.Boolean(compute='_check_ipf_planning')

    @api.one
    def _check_ipf_planning(self):
        try:
            planning = self.ipf_load_planning()
            if (planning and planning['source']) and 'BAR' in planning['source'] or 'PLV' in planning['source']:
                self.has_ipf_planning = True
            else:
                self.has_ipf_planning = False
        except Exception as e:
            _logger.warning('Error in IPF CASE integration.', exc_info=e)


    @api.multi
    def ipf_load_planning(self):
        self.ensure_one()
        res = None
        if self.is_jobseeker:
            personnummer = self.get_ais_a_pnr()
            if personnummer:
                try:
                    ipf = self.env.ref('ipf_planning.ipf_endpoint_planning').sudo()
                    res = ipf.call(personnummer=personnummer)
                except Exception as e:
                    _logger.warning('Error in IPF CASE integration.', exc_info=e)
        return res

    @api.multi
    def get_ais_a_pnr(self):
        try:
            if self.social_sec_nr:
                pnr = self.social_sec_nr.replace('-', '')
                return pnr
        except ValueError:
            raise UserError("Invalid personal identification number: %s" % self.social_sec_nr)

    def action_redirect_planning_url(self):
        """Invoked when 'Handlingsplan' button in Arbetsyta view is clicked."""
        self.ensure_one()
        url = ''
        planning = self.ipf_load_planning()
        if planning and planning['source']:
            if planning['source'] == 'PLV':
                url = 'http://ivs.arbetsformedlingen.se/etjanst/planeringsverktyg/#/start/bedomning/{}'.format(
                    self.social_sec_nr.replace('-', ''))
            elif planning['source'] == 'BAR':
                url = 'https://aobp.arbetsformedlingen.se:8443/prweb/PRAuth/HLPortal'
            if url:
                return {
                'type': 'ir.actions.act_url',
                'target': 'new',
                'url': url,
                }
