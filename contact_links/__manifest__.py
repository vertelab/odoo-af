# -*- coding: utf-8 -*-

{
    'name': 'AF Contact Links',
    'version': '12.0.1.2',
    'category': '',
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': [
        'contacts',
        'af_security',
        'hr_360_view'
    ],
    'data': [
        'security/security.xml',
        'views/res_partner_view.xml',
        'security/ir.model.access.csv',
        'data/server_action.xml',
        'data/partner.links.csv',
        # 'data/sync_link.xml'
    ],
    'demo': [
    ],
    'application': False,
    'installable': True,
}
