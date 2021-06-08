# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AF Demodata for Employees',
    'version': '12.0.0.1',
    'category': 'Human Resources',
    'sequence': 75,
    'summary': 'Adds demodata to the Employee module',
    'description': "",
    'website': 'https://www.odoo.com/page/employees',
    'images': [
        'images/hr_department.jpeg',
        'images/hr_employee.jpeg',
        'images/hr_job_position.jpeg',
        'static/src/img/default_image.png',
    ],
    'depends': [
        'base_setup',
        'hr',
    ],
    'data': [
        'data/hr_data_se.xml',
    ],
    'demo': [
        'data/hr_demo_se.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}