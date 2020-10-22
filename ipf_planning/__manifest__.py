# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Arbetssokande Planering',
    'summary': """ Innehåller de resurser Mina Sidor och ALF behöver från Planeringsverktyget och BÄR för Arbetssökandes planering""",
    'description': """
Jira
===========================================
AFC-1051 - Arbetssokande Planering (V12.0.1.0.0)
""",
    "version": "12.0.1.0.0",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": ["partner_view_360",
                "af_ipf", ],
    "external_dependencies": [],
    "data": [
        "views/partner_views.xml",
    ],
    "qweb": [
        "static/src/xml/planning.xml",
    ],
    "application": True,
    "installable": True,
}
