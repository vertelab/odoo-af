# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "IPF Case",
    "summary": "AF to IPF Arende For System integration",
    "version": "12.0.1.0.0",
    "author": "Arbetsförmedlingen",
    "license": "AGPL-3",
    'description': """
Jira
===========================================
AFC-2019 - Visa ärenden från BÄR i CRM (V12.0.1.0.0)
""",
    "website": "https://arbetsformedlingen.se/",
    "category": "Tools",
    "depends": ["partner_view_360",
                "af_ipf", ],
    "external_dependencies": [],
    "data": [
        "views/partner_views.xml",
        "data/case_data.xml",
    ],
    "application": True,
    "installable": True,
}
