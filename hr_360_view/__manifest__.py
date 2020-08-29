{
    'name': 'HR 360 View',
    'version': '12.0.0.1',
    'category': 'Human resources',
    'description': " AFC-667 - HR 360 View Module.",
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': ['base', 'hr', 'partner_view_360', 'contacts', 'partner_af_case', 'partner_daily_notes'],
    'data': [
        #'views/menu.xml',
        'views/hr_view.xml',
        'wizard/hr_employee_search_wizard.xml'
    ],
    'installable': True,
}
