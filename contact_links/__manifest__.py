# -*- coding: utf-8 -*-

{
    'name': 'Contact Links',
    'version': '12.0.1.1',
    'category': '',
    'description': """
Cases
===============================================================================
This module adds Links to a partner.

""",
    'author': 'Jupical',
    'license': 'AGPL-3',
    'depends': [
        'contacts',
    ],
    'data': [
        'security/security.xml',
		'views/res_partner_view.xml',
        'security/ir.model.access.csv',
        'data/server_action.xml',
    ],
    'demo': [
    ],
    'application': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
