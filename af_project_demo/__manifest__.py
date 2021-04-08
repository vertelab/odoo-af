  
# -*- coding: utf-8 -*-

{
    'name': 'Depreciated - AF BÄR with Project demodata',
    'version': '12.0.3',
    'website': 'https://www.odoo.com/page/project-management',
    'category': 'Project',
    'sequence': 10,
    'summary': 'Adds customized demodata to the project module ',
    'depends': [
        'base_setup',
        'project',
    ],
    'description': "Changed order of the name.",
    'data': [
        #'data/project_data_se.xml',
    ],
    # 'demo': ['data/project_demo_se.xml'],
    'test': [
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
