# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Arbetssokande Planering',
    "version": "12.0.2.1.2",
    'summary': """ Innehåller de resurser Mina Sidor och ALF behöver från Planeringsverktyget och BÄR för Arbetssökandes planering""",
    "description": """
Jira
===========================================
v12.0.1.0.1 AFC-734: Arbetssokande Planering Integration \n
v12.0.2.0.0 AFC-2239: Updated with get_ais_a_pnr function \n
v12.0.2.0.1 AFC-1051: Updated data file and index \n
v12.0.2.1.0 AFC-2305: Moved button 'Visa handlingsplan' and added redirect url function \n
v12.0.2.1.1 AFC-2474: Bugfix in function _check_ipf_planning \n
v12.0.2.1.2 AFC-2447: Handlingsplan icon place in the middle of the text. \n
""",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": ["partner_view_360",
                "af_ipf", ],
    "external_dependencies": [],
    "data": [
        "views/partner_views.xml",
        "data/planning_data.xml",
    ],
    "qweb": [
        "static/src/xml/planning.xml",
    ],
    "application": True,
    "installable": True,
}
