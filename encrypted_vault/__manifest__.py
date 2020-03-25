# Copyright 2017 - 2018 Modoolar <info@modoolar.com>
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
{
    'name': "Encrypted Vault",

    'summary': """
        This module uses encrypted fields to store sensitive credentials, and
        related information.""",
    'author': "Modoolar",
    'website': "https://modoolar.com",
    'category': 'Technical Settings',
    "version": "11.0.1.0.0",
    "license": "LGPL-3",
    "images": ["static/description/banner.png"],
    'depends': [
        'base_encrypted_field',
        'web_clipboard',
    ],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/encrypted_vault_data.xml',
        'views/encrypted_vault_history_view.xml',
        'views/encrypted_vault_view.xml',
        'views/encrypted_vault_custom_field_view.xml',
        "views/res_config_settings_view.xml",
        'views/actions.xml',
        'views/menu.xml',
    ],
    'external_dependencies': {
        'python': [
            'cryptography'
        ]
    },
    "application": True,
}
