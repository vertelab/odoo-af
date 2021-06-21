{
    'name': 'Partner KPI',
    'version': '12.0.1.1',
    'category': '',
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': [
        'partner_view_360'
    ],
    'data': [
        'views/res_partner_view.xml',
        'security/ir.model.access.csv'
    ],
    'application': False,
    'installable': True,
}
