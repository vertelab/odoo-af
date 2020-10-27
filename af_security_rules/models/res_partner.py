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
from odoo.tools import config
from pytz import timezone
from datetime import timedelta
from zeep.client import CachingClient
from zeep.helpers import serialize_object
from zeep import xsd
import traceback
from uuid import uuid4

import logging
_logger = logging.getLogger(__name__)

LOCAL_TZ = timezone('Europe/Stockholm')
WSDL_NYCKELTJANST = config.get(
    'bhtj_nyckeltjanst',
    'https://bhtj.arbetsformedlingen.se/KeyService/ws/nyckeltjanst?wsdl')
WSDL_INITIERANDE_NYCKELTJANST = config.get(
    'bhtj_initierande_nyckeltjanst',
    'https://bhtj.arbetsformedlingen.se/KeyService/ws/initierandenyckeltjanst?wsdl')
NYCKELTJANST = None
INITIERANDE_NYCKELTJANST = None
INIT_HEADER_SYSTEM_ID = 'CRM'
INIT_HEADER_API_VERSION = '1.3'


class BHTJModel(models.AbstractModel):
    _name = 'bhtj.model'
    _description = 'BHTJ Abstract Model'

    # This model makes it so that BHTJ is called when checking access rules for the inheriting model.
    # BHTJ data is then injected into context and used in field calculations for res.partner.
    # This is useful for models that will trigger a check of res.partner access rules, such as res.users.
    # The goal is to not call BHTJ more than once per server call.

    @api.model
    def _apply_ir_rules(self, query, mode='read'):
        """ Inject BHTJ data into context so we only run it once per call,
            instead of once per rule (or more!).
        """
        keys = self.env.user.sudo()._bhtj_get_user_keys()
        return super(
            BHTJModel, self.with_context(
                bhtj_keys=keys))._apply_ir_rules(
            query, mode=mode)

    @api.multi
    def check_access_rule(self, operation):
        """ Inject BHTJ data into context so we only run it once per call,
            instead of once per rule (or more!).
        """
        keys = self.env.user.sudo()._bhtj_get_user_keys()
        return super(BHTJModel, self.with_context(
            bhtj_keys=keys)).check_access_rule(operation)


class ResPartnerNotes(models.Model):
    _name = 'res.partner.notes'
    _inherit = ['res.partner.notes', 'bhtj.model']


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'bhtj.model']

    # Access rights to archive contacts. This is probably not good enough.
    # Can't specify read/write.
    # Can't specify domains per group (causes crossover between employers and jobseekers officers)
    # TODO: Look for a solution. Existing module or build one.
    #       Look at that encryption module to add new parameters to fields.
    active = fields.Boolean(
        groups='base.group_system,af_security.group_af_employers_high,af_security.group_af_jobseekers_high')
    jobseeker_access = fields.Selection(
        selection=[('STARK', 'Stark'), ('MYCKET_STARK', 'Mycket stark')],
        string='Access Level',
        compute='_compute_jobseeker_access',
        search='_search_jobseeker_access')

    @api.multi
    def _compute_jobseeker_access(self):
        """Compute jobseeker access level from BHTJ data."""
        keys = None
        for partner in self:
            # Only set a value for jobseekers.
            if partner.is_jobseeker:
                if not partner.social_sec_nr:
                    # We need a person number to continue
                    continue
                # Fetch keys from BHTJ
                if keys is None:
                    keys = self.env.user._bhtj_get_user_keys()
                # Match person number to BHTJ response.
                for access_level in keys.keys:
                    if partner.social_sec_nr in keys[access_level]:
                        partner.jobseeker_access = access_level

    @api.model
    def _search_jobseeker_access(self, op, value):
        """ Perform a search on the jobseeker_access field using data from BHTJ.
            :param op: the search operator.
            :param value: the search value.
            :returns: A new search domain matching BHTJ data.
        """
        _logger.debug(self.env.user)
        _logger.debug(self.env.context)
        #raise Warning('foobar')
        # BHTJ data injected in _apply_ir_rules
        if 'bhtj_keys' in self._context:
            keys = self._context.get(
                'bhtj_keys', {
                    'STARK': [], 'MYCKET_STARK': []})
        else:
            # New exiting path to get here. Try to find original user and
            # contact BHTJ.
            _logger.info(_("No BHTJ data in context. Extra call made."
                           "Additional models need to inherit bhtj.model."))
            _logger.debug(''.join(traceback.format_stack()))
            user = self._context.get('uid')
            user = user and self.env['res.users'].browse(user) or self.env.user
            keys = user._bhtj_get_user_keys()
        _logger.debug(keys)
        if op in ('=', '!='):
            if value in ('STARK', 'MYCKET_STARK'):
                pnr = keys[value]
            elif not value:
                pnr = keys['STARK'] + keys['MYCKET_STARK']
            if op == '=' and value:
                return [('social_sec_nr', 'in', pnr)]
            elif op == '=':
                return [('social_sec_nr', 'not in', pnr)]
            if op == '!=' and value:
                return [('social_sec_nr', 'not in', pnr)]
            elif op == '!=':
                return [('social_sec_nr', 'in', pnr)]
        if op in ('in', 'not in'):
            pnr = []
            for v in value:
                if v in ('STARK', 'MYCKET_STARK'):
                    pnr += keys[v]
                elif not v:
                    pnr += keys['STARK'] + keys['MYCKET_STARK']
                else:
                    # This value isn't supported
                    pnr = 'error'
                    break
            if pnr != 'error':
                _logger.debug(pnr)
                return [('social_sec_nr', op, pnr)]
        # This search is not supported. Let the developer (hopefully) know.
        raise Warning(_("res.partner._searchjobseeker_access: Search operator '%s'"
                        " and value '%s' has not been implemented yet.") % (op, value))

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        """Assign access rights when creating a jobseeker."""
        for vals in vals_list:
            if not vals.get('user_id'):
                vals['user_id'] = self.env.user.id
        return super(ResPartner, self).create(vals_list)

    @api.model
    def _bhtj_get_nyckeltjanst(self):
        """Fetch or initialize connection to BHTJ for checking access rights."""
        global NYCKELTJANST
        if NYCKELTJANST:
            return NYCKELTJANST
        try:
            key_service = CachingClient(WSDL_NYCKELTJANST)
            if not NYCKELTJANST:
                NYCKELTJANST = key_service
            return NYCKELTJANST
        except BaseException:
            # TODO: better logging
            raise Warning(
                _("Could not connect to BHTJ to check access rights!"))

    @api.model
    def _bhtj_get_initierande_nyckeltjanst(self):
        """Fetch or initialize connection to BHTJ for granting access rights."""
        global INITIERANDE_NYCKELTJANST
        if INITIERANDE_NYCKELTJANST:
            return INITIERANDE_NYCKELTJANST
        try:
            key_service = CachingClient(WSDL_INITIERANDE_NYCKELTJANST)
            if not INITIERANDE_NYCKELTJANST:
                INITIERANDE_NYCKELTJANST = key_service
            return INITIERANDE_NYCKELTJANST
        except BaseException:
            raise Warning(
                _("Could not connect to BHTJ to grant access rights!"))

    @api.multi
    def _grant_jobseeker_access(
            self,
            access_type,
            user=None,
            reason_code=None,
            reason=None,
            granting_user=None,
            start=None,
            interval=1):
        """ Grant temporary access to these jobseekers.
            :param access_type: The type of access. One of 'STARK' or 'MYCKET_STARK'.
            :param user: The user that is to be granted permission. Defaults to current user.
            :param reason_code: The reason code for granting extra permissions.
            :param reason: Freetext reason for granting extra permissions.
            :param granting_user: Optional. The user granting this access. Maybe?
            :param start: Datetime. The time when access is to start. Defaults to now. Works in mysterious ways.
            Past dates (time seems to be ignored) generates an error. Future times grant access immediately. Ignore it.
            :param interval: Integer. How many days access is to last. One of 1, 7, 14, 30, 60, 100 and 365.
            :returns: The BHTJ response as a Dict.
        """
        user = user or self.env.user
        start = start or fields.Datetime.now()
        pnr = []
        missing_pnr = []
        for partner in self:
            if partner.is_jobseeker and partner.social_sec_nr:
                pnr.append(partner.social_sec_nr.replace('-', ''))
            else:
                raise Warning(_("BHTJ: Partner %s is either not a jobseeker, or "
                                "is lacking a person number.") % partner.id)
        if not (interval in (1, 7, 14, 30, 60, 100, 365)):
            raise Warning(
                _("BHTJ: interval must be one of 1, 7, 14, 30, 60, 100, 365."))
        if not (reason or reason_code):
            raise Warning(_("BHTJ: You must provide a reason or reason_code."))
        if access_type not in ('STARK', 'MYCKET_STARK'):
            raise Warning(
                _("BHTJ: Access type must be either STARK or MYCKET STARK."))
        values = {
            '_soapheaders': {
                'apiVersion': INIT_HEADER_API_VERSION,
                'pisaID': granting_user and granting_user.login or '',
                'systemID': INIT_HEADER_SYSTEM_ID,
                'transactionID': uuid4()},
            'arbetssokandeLista': pnr,
            'giltigFran': start,
            'intervall': 'Dagar_%i' % interval,
            'orsak': {
                'friTxt': reason or '',
                'orsakKod': reason_code or '', },
            'nyckelTyp': access_type,
            'signatur': user.login
        }
        if reason_code:
            values['orsak']['orsakDef'] = 'NYKOD'
        else:
            values['orsak']['orsakDef'] = 'FRITXT'

        bhtj = self._bhtj_get_initierande_nyckeltjanst()
        _logger.debug('_grant_jobseeker_access: %s' % values)
        try:
            response = bhtj.service.skapaNyckel(**values)
            response = serialize_object(response, target_cls=dict)
        except BaseException:
            # TODO: Log error properly.
            raise Warning(_("Could not connect to BHTJ."))
        return response

    @api.model
    def af_security_install_rules(self):
        """Update existing rules that can't be changed through XML."""
        self.env.ref('base.res_partner_rule_private_employee').active = False


class User(models.Model):
    _inherit = 'res.users'

    @api.model
    def _bhtj_get_user_keys(self):
        """Fetch the jobseeker access rights of this user from BHTJ."""
        # TODO: This happens multiple times in one function call.
        # We need to cache this or BHTJ will get swamped.
        # DONE: Attempted to move to abstract model bhtj.model and inject
        # result into context.
        bhtj = self.partner_id._bhtj_get_nyckeltjanst()

        def normalize_pnr(pnr):
            return '%s-%s' % (pnr[:8], pnr[8:12])
        try:
            # Fetch keys from BHTJ
            response = bhtj.service.hamtaNyckelknippa(self.login)
            # Translate to a more usable structure.
            keys = {'STARK': [], 'MYCKET_STARK': []}
            for key in response:
                if key['nyckeltyp'] == 'Stark':
                    keys['STARK'].append(normalize_pnr(key['personnummer']))
                elif key['nyckeltyp'] == 'Mycket stark':
                    keys['MYCKET_STARK'].append(
                        normalize_pnr(key['personnummer']))
            return keys
        except BaseException:
            # TODO: Log error properly.
            raise Warning(_("Failed to connect to BHTJ!"))

    @api.model
    def _get_notes_edit_limit(self):
        return (fields.Datetime.now() - timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0)
