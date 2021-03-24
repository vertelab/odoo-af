# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "IPF AIS-Å ",
    "summary": "AF to IPF AIS Beslut Om Stod Read integration",
    "version": "12.0.1.1.0",
    "author": "Vertel AB",
    "license": "AGPL-3",
    'description': """
Jira
===========================================
V12.0.1.0.0 AFC-621: Integration Rusta-och-Matcha
v12.0.1.1.0 AFC-2001: Added start and stop date for AIS-Å
""",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": ["partner_view_360",
                "af_ipf", ],
    "external_dependencies": [],
    "data": [
        "views/partner_views.xml",
    ],
    "application": True,
    "installable": True,
}
