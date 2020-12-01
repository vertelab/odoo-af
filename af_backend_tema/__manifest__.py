# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Depreciated AF Backend Tema V12",
    "summary": "AF Backend Theme V12	",
    "version": "12.0.0.6",
    "category": "Theme/Backend",
    "description": """
		AF Backend tema för Odoo 12.0 community edition.
    """,
    "author": "Vertel AB",
    "license": "LGPL-3",
    "installable": "False",
    "depends": [
        "base", 'web'
    ],
    "qweb": [
        "static/src/xml/*.xml",
    ],
    "data": [
        'views/assets.xml',
        'views/template.xml',
        "views/web.xml"
    ]
}
