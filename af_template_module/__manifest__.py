{
    "name": "Af Template Module",
    "version": "12.0.1.0.1",
    "author": "Vertel AB",
    "maintainer": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    'description': """
Test Module \n
======================================================\n
This module is maintained from: https://github.com/vertelab/odoo-af/edit/Dev-12.0/af_template_module/ 
Hover over fields to se a brief description of them \n
For more information make sure you are in debug mode \n
v12.0.1.0 - AFC-123 Added the module to the repo \n

""",
    "depends": [
        'contacts'
    ],
    "external_dependencies": [
    ],
    "data": [
        'views/res_partner.xml',
        'security/ir.model.access.csv' 
    ],
    "application": False,
    "installable": True,
}
