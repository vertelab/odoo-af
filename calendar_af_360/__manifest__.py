# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Calendar management - AF (360)",
    "version": "12.0.1.0.4",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    'description': """
Extension module for AF appointments \n
================================================================================================ \n
This module extends the functionality regarding appointments functionality \n
This functionality is tailored for AF. \n
v12.0.1.0.1: versions before good version control \n
v12.0.1.0.2 AFC-2113: Updated how res.users is presented in views. \n
v12.0.1.0.3 AFC-2278: Updated critera for shown meetings \n
v12.0.1.0.4 AFC-2440: Added dependency to ipf_ais_bos \n
\n
""",
    "depends": [
        "calendar_af",
        "partner_view_360",
        "ipf_ais_bos",
        "hr_360_view",
    ],
    "external_dependencies": [],
    "data": [
        "views/calendar_occasion_view.xml",
        "views/res_partner_view.xml",
        "views/hr_employee_view.xml",
        "views/calendar_occasion_view.xml",
        "views/calendar_appointment_view.xml",
    ],
    "application": False,
    "installable": True,
}
