{
    'name': 'HR 360 View',
    'summary': """
        A dashboard for employees to search for job seekers.
        """,
    'version': '12.0.0.8',
    'category': 'Human resources',
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': [
        'hr',
        'partner_view_360',
        # 'partner_af_case',
        # 'partner_daily_notes', removed dependency
        'hr_employee_firstname_extension',
        'af_ipf',
    ],
    'data': [
        # 'views/menu.xml',
        'views/hr_view.xml',
        'wizard/hr_employee_search_wizard.xml'
    ],
    'installable': True,
}
