# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "AF Security Rules",
    "version": "12.0.1.2.0",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "description": """Security rules for Arbetsförmedlingen.
=======
v12.0.1.1.1 AFC-2168: Changed groups of various menus.
v12.0.1.1.2 AFC-2227: Fixed a bug when finding logged in user.
v12.0.1.1.3 AFC-2239: Hid menu Lokalkontor.
v12.0.1.2.0 AFC-2298: Fixed access rights. jobseeker_officer, meeting_planner, and meeting_admin.
    """,
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": [
        "af_security",
        "partner_view_360",
        "partner_daily_notes",
        "calendar_af",
        "mail",
        "contacts",
        "hr_holidays",
        "sms",
        "hr_office",
        ],
    "external_dependencies": {'python': ['zeep']},
    "data": [
        "security/af_security.xml",
        "security/ir.model.access.csv",
        'data/menu.xml',
    ],
    "application": True,
    "installable": True,
}
