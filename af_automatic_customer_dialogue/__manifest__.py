# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Af Automatic Customer Dialogue',
    'summary': "Af Automatic Customer Dialogue",
    'version': '12.0.1.1',
    'author': "Vertel AB",
    'license': "AGPL-3",
    'maintainer': 'Vertel',
    'website': 'http://www.vertel.',
    'depends': ['base_setup', 'mail', 'partner_daily_notes'],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/menuitem.xml',
        'views/partner_event_view.xml',
        'data/mail_template.xml',
        'data/data.xml',
    ],
    'auto_install': False,
    'installable': True,
}
