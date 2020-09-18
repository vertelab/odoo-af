{
    'name': 'HR 360 View',
    'version': '12.0.0.4',
    'category': 'Human resources',
      "description": """
	 v12.0.0.1 AFC-667 - HR 360 View Module. Lägger till huvudsida för handläggare med sökyta samt flikar med uppgifter centrerade från handläggaren.
	 v12.0.0.2 AFC-713 - Bytt namn från Handläggaryta till Arbetsyta enligt beslut från Införandegruppen. Dolt menyn HR 360.
	 v12.0.0.3 AFC-715 - Lagt till rubrik på vyn för Arbetsyta.
	 v12.0.0.4 AFC-715 - Lade till beroende på Firstname Extension som döljer förnamn-efternamn-fälten i visningsläge.
    """,
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': [
      'hr', 
      'partner_view_360', 
      'partner_af_case', 
      'partner_daily_notes',
      'hr_employee_firstname_extension'],
    'data': [
      #'views/menu.xml',
      'views/hr_view.xml',
      'wizard/hr_employee_search_wizard.xml'
    ],
    'installable': True,
}
