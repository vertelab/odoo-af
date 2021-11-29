# -*- coding: utf-8 -*-
# Copyright 2021 - TODAY, Arbetsförmedlingen, (https://arbetsformedlingen.se)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class Arbetssokande(models.Model):
    _inherit = 'arbetssokande'

    genomforande_ids = fields.One2many(comodel_name='arbetssokande.genomforande',
                                       string='Genomforande',
                                       inverse_name="customer_id",
                                       compute='compute_genomforande_ids')

    @api.multi
    def compute_genomforande_ids(self):
        for record in self:
            personnummer = record.get_case_pnr()
            if personnummer:
                try:
                    # For future use when integrating Cases
                    # ipf = self.env.ref('ipf_case.ipf_endpoint_case').sudo()
                    # res = ipf.call(personnummer=personnummer)
                    # record.case_ids = record.env['res.partner.case']
                    # for arende in res.get('arenden', []):
                    # record.case_ids |= record.env['res.partner.case'].create_arende(arende, record.id)

                    ipf = self.env.ref('ipf_genomforande.ipf_endpoint_genomforanden').sudo()
                    res = ipf.call(personnummer=personnummer)
                    for genomforande in res.get('genomforanden', []):
                        record.genomforande_ids |= record.env['arbetssokande.genomforande'].create_genomforande(
                            genomforande,
                            record.id)

                except Exception as e:
                    _logger.warning('Error in IPF Genomforande integration.', exc_info=e)
                    record.genomforande_ids = None

    @api.multi
    def get_case_pnr(self):
        try:
            if self.personnummer:
                pnr = self.personnummer.replace('-', '')
                return pnr
        except ValueError:
            raise UserError("Invalid personal identification number: %s" % self.personnummer)
