# -*- coding: utf-8 -*-

{
    'name': 'Contact Links',
    'version': '12.0.1.1',
    'category': '',
    'description': """
Cases
===============================================================================
This module adds Links to a partner.
Added server action 'Update Link' to add all links in contact.Select contacts in which you want to add links and click on
Actions -> Update Link. If you can't see 'Update Link' inside Action then Go to Setting >> Technical >> Actions >> Server
Actions and search 'Update Link'. Open it and click on 'Create Contexual Action' button then refresh browser.

""",
    'author': 'Jupical',
    'license': 'AGPL-3',
    'depends': [
        'contacts', 'af_security'
    ],
    'data': [
        'security/security.xml',
		'views/res_partner_view.xml',
        'security/ir.model.access.csv',
        'data/server_action.xml',
        'data/partner.links.csv'
    ],
    'demo': [
    ],
    'application': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
