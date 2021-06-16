# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "AF web gui",
    "version": "12.0.1.0.2",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "description": """
AF web gui
Used to override GUI in odoo core
===========================================
v12.0.1.0.0 AFC-2260: Introduced module
v12.0.1.0.1 AFC-2390: Changed module name and description. Changed title and favicon
v12.0.1.0.2 AFC-2389: Changed default behaviour of the popup notification
""",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": ["web"],
    "external_dependencies": [],
    "data": [
        "views/assets.xml",
        "views/layout.xml"
    ],
    "qweb": [
        "static/src/xml/dialog.xml",
    ],
    "application": False,
    "installable": True,
}
