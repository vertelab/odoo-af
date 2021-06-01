# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "AF web crash manager",
    "version": "12.0.1.0.0",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "description": """
AF web crash manager
Used to override javascripts from odoo's crash manager javascript.
===========================================
v12.0.1.0.0 AFC-2260: Introduced module
""",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": ["web"],
    "external_dependencies": [],
    "data": [
        "views/assets.xml"
    ],
    "qweb": [
        "static/src/xml/dialog.xml",
    ],
    "application": False,
    "installable": True,
}
