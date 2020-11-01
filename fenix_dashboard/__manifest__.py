{
    "name": "Fenix Dashboard",
    "version": "12.0.0.0",
    "description": """
     This module shows the dashbord of an employee´s daily work.
""",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        "project"
    ],
    "data": [
        "views/af_dashboard.xml",
        "security/ir.model.access.csv",
        "security/security.xml"
    ],
    'post_init_hook': 'post_init_hook',
    "application": False,
    "installable": True,
}
