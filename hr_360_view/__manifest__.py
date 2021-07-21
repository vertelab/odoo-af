{
    'name': 'HR 360 View',
    'summary': """
        A dashboard for employees to search for job seekers.
        """,
    'version': '12.0.2.2.6',
    'category': 'Human resources',
    'description': """
""",
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': [
        'hr',
        'partner_view_360',
        'hr_employee_firstname_extension',
        'af_ipf',
    ],
    'data': [
        'views/hr_view.xml',
        'wizard/hr_employee_search_wizard.xml'
    ],
    'installable': True,
    'application': False,
}
