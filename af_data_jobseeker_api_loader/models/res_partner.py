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
import os

from odoo.tools import config
from odoo import models, fields, api, _
from odoo.tools.profiler import profile

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def create_jobseekers(self):
        path = os.path.join(
            config.options.get('data_dir'),
            'AIS-F/arbetssokande.csv')
        path = "/usr/share/odoo-af/af_data_jobseeker_api_loader/data/test_dumps/arbetssokande.csv" # testing purposes only
        self.create_partners_from_api('SOKANDE_ID', path)

    @api.model
    def create_partners_from_api(self, key, path):
        db_con = self.env.ref('af_ipf.ipf_endpoint_rask').sudo()
        db_values = {'res.country.state': self.search('res.country.state', 'code', 'id'),
                     'hr.departement': self.search('hr_department', 'office_code', 'id'),
                     'res.sun': self.search('res.sun', 'code', 'id'),
                     'res.partner.skat': self.search('res.partner.skat', 'code', 'id'),
                     'res.partner.education_level': self.search('res.partner.education_level', 'name', 'id'),
                     'res.users': self.search('res.users', 'login', 'id'),
                     'res.country': self.search('res_country', 'name', 'id', 'lang="sv_SE"'),}
        index = 0
        iterations = 0
        with open(path) as fh:
            for row in fh:
                if index == 0:
                    header = {key.strip():index for index, key in
                              enumerate(row.strip().split(','))}
                    try:
                        id_index = header[key]
                    except KeyError:
                        _logger.error(
                            f'Failed to find {key} in {", ".join(header)}')
                        raise
                    continue
                customer_id = row.strip.split(',')[id_index]
                if not self.env['res.partner'].search_count(['customer_id',
                                                             '=',
                                                             customer_id]):
                    self.env['res.partner'].rask_as_get(
                        customer_id, db_con, db_values)

                iterations += 1
                if iterations > 500:
                    self.env.cr.commit()
                    iterations = 0

    def search(self, obj, key, field_name, context=None):
        """Build dicts with key: field_name"""
        if context:
            return {res[key]: res[field_name] for res in
                    self.env[obj].with_context(eval(context)).search_read(
                        [], [key, field_name])}
        return {res[key]: res[field_name] for res in
                self.env[obj].search_read([], [key, field_name])}
