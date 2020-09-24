# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Calendar management - AF (360)",
    "version": "12.0.1.0.1",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": ["calendar_af", "partner_view_360", 'hr_360_view'],
    "external_dependencies": [
    ],
    "data": [
        "views/res_partner_view.xml",
        "views/hr_employee_view.xml",
    ],
    "application": False,
    "installable": True,
}
