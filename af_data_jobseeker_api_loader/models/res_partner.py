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

LOAD_AISF_ASOK_PROCESS = "LOAD AIS-F ASOK"

class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def create_jobseekers(self, path):
        _logger.info("LOAD AIS-F Jobseekers %s - START" % path)
        if not path:
            path = os.path.join(
                config.options.get('data_dir'),
                'AIS-F/arbetssokande.csv')
            path = "/usr/share/odoo-af/af_data_jobseeker_api_loader/data/test_dumps/arbetssokande.csv" # testing purposes only
        self.create_partners_from_api(path)
        _logger.info("LOAD AIS-F Jobseekers %s - END" % path)

    @api.model
    def create_partners_from_api(self, path):
        db_con = self.env.ref('af_ipf.ipf_endpoint_rask').sudo()
        db_values = {'res.country.state': self.search_model('res.country.state', 'code', 'id'),
                     'hr.department': self.search_model('hr.department', 'office_code', 'id'),
                     'res.sun': self.search_model('res.sun', 'code', 'id'),
                     'res.partner.skat': self.search_model('res.partner.skat', 'code', 'id'),
                     'education_level': self.search_model('res.partner.education.education_level', 'name', 'id'),
                     'res.users': self.search_model('res.users', 'login', 'id'),
                     'res.country': self.search_model('res.country', 'name', 'id', {'lang':'sv_SE'})
                     }
        filename = os.path.basename(path)
        process_name = LOAD_AISF_ASOK_PROCESS + " " + filename

        with open(path) as fh:
            for row in fh:
                customer_id = row.rstrip("\n")

                self.env['af.process.log'].log_message(
                    process_name, customer_id, "PROCESS INITIATED", message=customer_id,
                    additional_message='0', objectid=customer_id, first=True)

                self.env["res.partner"]._aisf_sync_jobseeker(
                    db_values,
                    process_name,
                    customer_id,
                    customer_id
                )

    def search_model(self, obj, key, field_name, context=None):
        """Build dicts with key: field_name"""
        if context:
            return {res[key]: res[field_name] for res in
                    self.env[obj].with_context(**context).search_read(
                        [], [key, field_name])}
        return {res[key]: res[field_name] for res in
                self.env[obj].search_read([], [key, field_name])}
