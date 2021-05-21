# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "AF Security",
    "version": "12.0.1.0.2",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "description": """
    User groups for Arbetsförmedlingen. n\
    This module is maintained from https://github.com/vertelab/odoo-af \n
    """
     ,
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        "contacts",
        'hr_office',
        ],
    "external_dependencies": {'python': ['zeep']},
    "data": [
        "security/af_security.xml",
        "views/res_users.xml",
        "views/ir_actions.xml",
    ],
    "application": True,
    "installable": True,
}
