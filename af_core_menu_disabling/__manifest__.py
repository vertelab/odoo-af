# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': "Disable access for core menus",
    'summary': "Hide some specific menus for internal type of user.",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    'category': 'Tools',
    'version': '12.0.1.0',
    'depends': ['calendar', 'website', 'contacts'],
    'data': [
        'security/security_view.xml',
    ],
    "application": False,
    "installable": True,
}
