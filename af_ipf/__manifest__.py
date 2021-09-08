# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "AF IPF Integration",
    "version": "12.0.2.0.0",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "summary": "Module for synchronous integrations to IPF",
    "description": """
Jira
===========================================
v12.0.1.0.1 AFC-734: Integration till IPF
v12.0.1.0.2 AFC-1385: Data för rask integration
v12.0.1.0.3 AFC-2001: updated default IPF url
v12.0.1.0.4 AFC-2239: Fixed bug for getting users
v12.0.1.0.5 AFC-1051: Moved data files to respective modules
v12.0.1.0.6 AFC-2550: Fixed bug in response
v12.0.1.0.7 AFC-2543: Updated get_ssl_params method
v12.0.2.0.0 AFC-2532: Added Mask data file
""",
    "depends": ["af_security"],
    "external_dependencies": {"python": ["requests"]},
    "data": [
        "views/ipf_views.xml",
        "data/customer_data.xml",
        "data/rask_data.xml",
        "data/mask_data.xml",
        "security/ir.model.access.csv",
    ],
    "application": True,
    "installable": True,
}
