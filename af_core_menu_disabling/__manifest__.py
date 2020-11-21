# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': "Disable access for core menus",
    'summary': "Hides core menus for internal users.",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    'category': 'Tools',
    'version': '12.0.1.1',
    'depends': ['calendar','website','contacts'],
    "description": """
        This module adds a hides core menues for users in the group internal-users.\n
        It also adds a group to Show the hidden menues. \n
    """,
    'data': [
        'security/security_view.xml',
    ],
    "application": False,
    "installable": True,
}
