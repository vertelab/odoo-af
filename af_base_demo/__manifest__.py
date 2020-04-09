{
    'name': 'AF Base Demodata',
    'version': '12.0.0.1',						
    'category': '',
    'description': """
Module to overright Odoo original demodata.
===========================================================
AFC-119

""",
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': ['base'],
    'demo': [
			'data/base.partner.demo.se.xml',
            'data/res.country.state.se.csv',
			'res_company_data.se.xml'
        ],
    'application': False,
    'installable': True,
}