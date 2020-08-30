{
    'name': 'AF Odoo Demodata translation',
    'version': '12.0.0.4',						
    'category': '',
    'description': """
Module overwrites Odoos original demodata with swedish data.\n
===========================================================\n
AFC-119\n
\n
\n
v12.0.1.4  - Moved content of the module from af_base_demo to this module, since the files here contain "Af CRM generated" testdata. \n
\n
\n
""",
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': ['base'],
    'demo': [
			'data/base_partner_demo_se.xml',
            #'data/res.country.state.se.csv',
			#'data/res_company_data_se.xml',
			#'data/res_company_data_se.xml',
			#'data/res_partner_image_demo_se.xml',
			#'data/res_users_demo_se.xml'			
        ],
    'application': False,
    'installable': True,
}