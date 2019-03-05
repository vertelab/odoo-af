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
    _inherit = 'project.issue'

    # ~ sudo_id = fields.Many2one(comodel_name='res.users',string='Login as', domain=lambda u: [('partner_id.commercial_partner_id','=','commercial_partner_id'), ('groups_id','not in', u.env.ref('base.group_user'))])
    sudo_id = fields.Many2one(comodel_name='res.users',string='Login as', domain=lambda u: [('groups_id','not in', u.env.ref('base.group_user').id)])
    commercial_partner_id = fields.Many2one(comodel_name='res.partner',related='partner_id.commercial_partner_id')
    
    @api.multi
    def write(self, values):
        if 'partner_id' in values.keys():
            partner = self.env['res.partner'].browse(values['partner_id'])
            # ~ users = self.env['res.users'].search([('partner_id.commercial_partner_id','=',partner.commercial_partner_id.id)]).filtered(lambda u: self.env.ref('base.group_user') not in u.groups_id)
            # ~ values['sudo_ids'] = [(6,0,users.mapped('id'))]
        res = super(project_issue, self).write(values)
        return res

    @api.multi
    def sudo_login(self,):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': '/',
            'target': 'new',
        }
        # ~ raise Warning('Hello %s' % self.sudo_id)
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
