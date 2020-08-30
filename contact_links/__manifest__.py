# -*- coding: utf-8 -*-

{
    'name': 'AF Contact Links',
    'version': '12.0.1.2',
    'category': '',
    'description': """
Cases
===============================================================================
This module adds Links to a partner.
Added server action 'Update Link' to add all links in contact.Select contacts in which you want to add links and click on
Actions -> Update Link. If you can't see 'Update Link' inside Action then Go to Setting >> Technical >> Actions >> Server
Actions and search 'Update Link'. Open it and click on 'Create Contexual Action' button then refresh browser.

v12.0.1.2	- Updated manifest and added Af-logo to description. \n
			- Updated the security-groups in the datafile to match new version of af_security-groups. \n
\n
""",
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
        #'data/sync_link.xml'
    ],
    'demo': [
    ],
    'application': False,
    'installable': True,
}
