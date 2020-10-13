# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "IPF AIS-Å ",
    "version": "12.0.1.0.0",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": ["partner_view_360", ],
    "external_dependencies": [],
    "data": [
        "views/partner_views.xml",
    ],
    'qweb': [
        'static/src/xml/ais_a.xml',
    ],
    "application": True,
    "installable": True,
}
