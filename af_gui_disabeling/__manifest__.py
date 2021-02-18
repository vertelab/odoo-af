{
    "name": "Replaced by web_gui_disabeling_af",
    "version": "12.0.0.0",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
	"description": """
	 v12.0.0.0 AFC-1225 Hide settings for the logged in user
	 This module is replaced by odoo-web/web_gui_disabeling_af
    """,
    "depends": ["base"],
    "external_dependencies": [],
    "data": [
        'views/assets.xml'
    ],
    'qweb': [
        "static/src/xml/base.xml",
        ],
    "application": True,
    "installable": False,
}
