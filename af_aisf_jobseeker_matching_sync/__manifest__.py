#  Copyright (c) 2021 Arbetsförmedlingen.

{
    'name': 'AIS-F Jobseeker Sync',
    'version': '12.0.0.2.2',
    'summary': 'Sync Jobseeker data from AIS-F.',
    'description': """AIS-F sync
================================================================================================
v12.0.0.1.0: AIS-F sync implemented.\n
v12.0.0.2.0 AFC-2245: Added better handling of jobseekers with SPU. \n
v12.0.0.2.1 AFC-2254: Misc changes \n
v12.0.0.2.2 AFC-2263: Changed boolean to selection field \n
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
