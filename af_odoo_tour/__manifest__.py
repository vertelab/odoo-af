{
    'name': 'Af CRM Introduction tour',
    'version': '12.0.0.0',
    "description": """
       AFC-780 v 12.0.0.0 This module hosts all introduction tours to Af CRM.
    """,
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': ['daily_notes', 
				'calendar_af', 
				'partner_daily_notes'],
    'data': [
        'data/data.xml',
        'wizard/intoduction_wizard.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
}
