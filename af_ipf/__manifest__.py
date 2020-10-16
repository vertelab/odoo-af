# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "AF IPF Integration",
    "version": "12.0.1.0.1",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "summary": "Module for synchronous integrations to IPF",
    'description': """
Jira
===========================================
AFC-734 Integration till AIS-Å (V12.0.2.0.0)
""",
    "depends": ["af_security"],
    "external_dependencies": {'python': ['requests']},
    "data": [
        "views/ipf_views.xml",
        "data/customer_data.xml",
        "data/ais_a_data.xml",
        #"data/planning_data.xml",
    ],
    "application": True,
    "installable": True,
}
