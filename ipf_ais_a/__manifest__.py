# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "IPF AIS-Å ",
    'summary': """Integration till AIS-Å""",
    "version": "12.0.1.0.0",
    "author": "Vertel AB",
    "license": "AGPL-3",
    'description': """
Jira
===========================================
AFC-621 - Integration Rusta-och-Matcha (V12.0.1.0.0)
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
