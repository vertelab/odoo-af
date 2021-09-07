# -*- coding: utf-8 -*-

{
    'name': 'AF Contact Links',
    'version': '12.0.0.2.3',
    'category': '',
    'description': """
Cases
===============================================================================
This module adds Links to for a partner. \n
Added server action 'Update Link' to add all links in contact.Select contacts in which you want to add links and click on \n
Actions -> Update Link. If you can't see 'Update Link' inside Action then Go to Setting >> Technical >> Actions >> Server \n
Actions and search 'Update Link'. Open it and click on 'Create Contexual Action' button then refresh browser. \n
 \n
The links in the module works in production.  \n
For links in test environments see the readme.rst-file for instruction.  \n
Links that are nor working are prefixed with 'n/a' to illustrate that they are not working yet.  \n
 \n
v12.0.0.1.2: Updated manifest and added Af-logo to description. \n
             Updated the security-groups in the datafile to match new version of af_security-groups. \n
v12.0.0.1.4: Made sure the contact links are computed with the customer number\n
v12.0.0.1.5: Updated link URLs. \n
v12.0.0.1.6: Added AIS link. \n
v12.0.0.2.0 AFC-2229: Added sort order for links. \n
v12.0.0.2.1 AFC-2254: Updated URL for a few links. \n
v12.0.0.2.2 AFC-2537: Updated URL for a link. \n
v12.0.0.2.3 AFC-2711: Fixed error when create a new job seeker or employee. \n

""",
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': [
        'contacts',
        'af_security',
        'hr_360_view',
        'partner_view_360',
    ],
    'data': [
        'security/security.xml',
        'views/res_partner_view.xml',
        'security/ir.model.access.csv',
        'data/partner.links.csv',
    ],
    'demo': [
    ],
    'qweb': [
        'static/src/xml/contact_links.xml'
    ],
    'application': False,
    'installable': True,
}
