#  Copyright (c) 2021 Arbetsförmedlingen.

{
    'name': 'AIS-F Jobseeker Sync',
    'version': '12.0.0.3.0',
    'summary': 'Sync Jobseeker data from AIS-F.',
    'description': """AIS-F sync
================================================================================================
v12.0.0.1.0: AIS-F sync implemented.\n
v12.0.0.2.0 AFC-2245: Added better handling of jobseekers with SPU. \n
v12.0.0.2.1 AFC-2254: Misc changes \n
v12.0.0.2.2 AFC-2263: Changed boolean to selection field \n
v12.0.0.2.3 AFC-2324: Enabled multiple next contact types \n
v12.0.0.2.4 AFC-2675: Fixed error handling and logging \n
v12.0.0.3.0 AFC-2728: Added fields for res.arbetssokande \n
""",
    'category': 'Technical Settings',
    'author': 'Vertel AB',
    'website': 'https://vertel.se',
    'license': 'AGPL-3',
    'depends': ['af_process_log', 'af_ipf', 'res_arbetssokande', 'partner_education'],
    'data': [],
    'demo': [],
    'installable': True,
    'auto_install': False
}
