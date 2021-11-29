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


class ArbetssokandeGenomforande(models.TransientModel):
    _name = 'arbetssokande.genomforande'
    _description = 'Genomförande För System'

    customer_id = fields.Many2one(
        comodel_name="arbetssokande", string="Arbetssökande")
    source = fields.Char(string='Source')
    refers_to = fields.Char(string='Refers to')
    status = fields.Char(string='Status')
    start = fields.Date(string='Start date')
    stop = fields.Date(string='End date')
    source = fields.Char(string='Source')
    extent = fields.Char(string='Extent')
    organiser = fields.Char(string='Organiser')

    @api.model
    def create_genomforande(self, vals, customer_id):

        start_date = vals.get('genomforande_period', {}).get('startdatum')
        stop_date = vals.get('genomforande_period', {}).get('slutdatum')
        support_type_short = vals.get('stodtyp_forkortning')
        case_type_short = vals.get('arendetyp_kortnamn')
        extent = vals.get('tjanstgoringsgrad')
        status = vals.get('genomforande_fas')
        organiser = vals.get('anordnare', {}).get('arbetsstalle_organisationsnummer')

        if len(vals['arende_id']) > 8:
            source = 'BÄR'
        else:
            source = 'AIS'

        if support_type_short:
            refers_to = f'{case_type_short} ({support_type_short})'
        else:
            refers_to = case_type_short

        if status == 'Inväntar periodstart':
            status = 'Väntar'
        elif status == 'Genomförandeperiod':
            status = 'Genomförande'
        elif status == 'Period avslutas':
            status = 'Avslutad'

        return self.create({
            'customer_id': customer_id,
            'source': source,
            'refers_to': refers_to,
            'status': status,
            'start': datetime.strptime(start_date, '%Y-%m-%d') if start_date else False,
            'stop': datetime.strptime(stop_date, '%Y-%m-%d') if stop_date else False,
            'extent': f'{extent} %' if extent is not None else '',
            'organiser': f'{organiser[:6]}-{organiser[6:]}' if organiser is not None else '',
        })
