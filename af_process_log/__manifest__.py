#  Copyright (c) 2021 Arbetsförmedlingen.

{
    'name': 'AF Process Log',
    'version': '12.0.0.1.0',
    'summary': 'Provides a log object for AF processes.',
    'description': '''v12.0.1.0  - Process log module created.''',
    'category': 'Technical Settings',
    'author': 'Vertel AB',
    'website': 'https://vertel.se',
    'license': 'Other proprietary',
    'depends': ['web'],
    'data': [
        "security/ir.model.access.csv",
        "views/af_process_log.xml",
    ],
    'demo': [],
    'installable': True,
    'auto_install': False
}
