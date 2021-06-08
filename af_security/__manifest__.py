# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "AF Security",
    "version": "12.0.1.1.0",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "description": """
User groups for Arbetsförmedlingen. n\
This module is maintained from https://github.com/vertelab/odoo-af \n
================================================================================================ \n
This functionality is tailored for AF. \n
v12.0.1.0.2: versions before good version control \n
v12.0.1.0.3: added .js to remove core context options \n
v12.0.1.1.0: Changed translation to prepare for removal of ADKD Automatic Editor role \n
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
        "views/assets.xml",
    ],
    "application": True,
    "installable": True,
}
