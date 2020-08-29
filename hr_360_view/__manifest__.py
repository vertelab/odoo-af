{
    'name': 'HR 360 View',
    'version': '12.0.0.2',
    'category': 'Human resources',
      "description": """
	 v12.0.0.1 AFC-667 - HR 360 View Module. Lägger till huvudsida för handläggare med sökyta samt flikar med uppgifter centrerade från handläggaren.
	 v12.0.0.2 AFC-713 - Bytt namn från Handläggaryta till Arbetsyta enligt beslut från Införandegruppen. Dolt menyn HR 360.
    """,
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': ['base', 'hr', 'partner_view_360', 'contacts', 'partner_af_case', 'partner_daily_notes', 'af_security'],
    'data': [
        #'views/menu.xml',
        'views/hr_view.xml',
        'wizard/hr_employee_search_wizard.xml'
    ],
    'installable': True,
}
