# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "AF Security",
    "version": "12.0.1.0.1",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "description": "User groups for Arbetsförmedlingen.",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        "contacts",
        'hr',
        ],
    "external_dependencies": {'python': ['zeep']},
    "data": [
        "security/af_security.xml",
        "views/hr_views.xml",
        "views/res_users.xml",
    ],
    "application": True,
    "installable": True,
}
