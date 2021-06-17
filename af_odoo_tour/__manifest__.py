{
    'name': 'Af CRM Introduction tour',
    'version': '12.0.0.1',
    "description": """
       v 12.0.0.0 AFC-780  This module hosts all introduction tours to Af CRM. \n
       v 12.0.0.1 AFC-2266 Updated format of person number for searching. \n
    """,
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': [
				'calendar_af', 
				'calendar_af_360', 
				'partner_daily_notes'],
    'data': [
        'data/data.xml',
        'wizard/intoduction_wizard.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
}
