#  Copyright (c) 2021 Arbetsförmedlingen.

{
    'name': 'AIS-F Jobseeker Sync',
    'version': '12.0.0.2.0',
    'summary': 'Sync Jobseeker data from AIS-F.',
    'description': """AIS-F sync
================================================================================================
v12.0.0.1.0: AIS-F sync implemented.\n
v12.0.0.2.0 AFC-2245: Added better handling of jobseekers with SPU. \n
""",
    'category': 'Technical Settings',
    'author': 'Vertel AB',
    'website': 'https://vertel.se',
    'license': 'AGPL-3',
    'depends': ['af_process_log', 'af_ipf', 'partner_view_360', 'partner_education'],
    'data': [],
    'demo': [],
    'installable': True,
    'auto_install': False
}
