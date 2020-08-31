{
    "name": "Test Module",
    "version": "12.0.1.0.1",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    'description': """
Test Module
===============================================================================
Hover over fields to se a brief description of them
For more information make sure you are in debug mode
""",
    "depends": [
        'contacts'
    ],
    "external_dependencies": [
    ],
    "data": [
        'views/res_partner.xml',
        'security/ir.model.access.csv' 
    ],
    "application": False,
    "installable": True,
}
