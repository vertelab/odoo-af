{
    'name': 'HR Jobseeker',
    'version': '12.0.0.1',
    'category': 'Human resources',
    'description': """
	 v12.0.0.1 AFC-1286 - Jobseeker.
    """,
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': ['base', 'hr', 'mail'],
    'data': [
        'security/ir.model.access.csv',

        'views/menu_item.xml',
        'views/job_seeker_view.xml',
        'views/job_seeker_stage_view.xml',

        'data/data.xml',

    ],
    'installable': True,
}
