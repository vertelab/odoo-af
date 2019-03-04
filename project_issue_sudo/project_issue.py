 #-*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2019- Vertel AB.
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


from openerp import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class project_issue(models.Model):
    _inherit = 'product.issue'

    sudo_ids = fields.Many2many(comodel_name='res.users',string='Login as')
    
    @api.multi
    def write(self, values):
        if 'partner_id' in values.keys():
            partner = self.env['res.partner'].browse(values['partner_id'])
            users = self.env['res.users'].search([('partner_id.commercial_partner_id','=',partner.commercial_partner_id)]).filtered(lambda u: self.env.ref('base.group_user').id not in u.groups_id)
            values['sudo_ids'] = [(6,0,users.mapped('id')]
        res = super(project_issue, self).write(values)
        return res

    @api.multi
    def sudo_login(self,):
        raise Warning('Hello %s' % self.sudo_ids)
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
