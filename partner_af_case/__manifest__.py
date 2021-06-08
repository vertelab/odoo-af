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

{
    'name': 'Depreciated Af Cases',
    'version': '12.0.1.2',
    'category': '',
    'description': """
Depreciated Af Cases
===============================================================================
v12.0.1.1 AFC-185, 199
This module adds cases to a partner.

v12.0.1.2 Lagt till översättningar som saknades.

""",
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': [
        'base_map',
        'partner_view_360',
        'hr_360_view',
    ],
    'data': [
        'views/res_partner_view.xml',
        'security/ir.model.access.csv',
        'views/res_partner_notes_view.xml',
        # 'data/ir.model.fields.csv',
    ],
    'demo': [
    ],
    'application': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
