# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Calendar management - AF Reports",
    "version": "12.0.2.0.0",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "summary": "Calendar management - reports",
    'description': """
Module for AF appointments reports
================================================================================================
This module adds new reports related to appointments functionality \n
This functionality is tailored for AF. \n
v12.0.1.0.0: versions before good version control \n
v12.0.2.0.0 AFC-1805: Major overhaul of functionality. PDM occasions now handled differently. \n
\n
""",
    "depends": [
        "calendar_af",
    ],
    "external_dependencies": [
    ],
    "data": [
        "security/ir.model.access.csv",
        "report/calendar_report_views.xml",
        "report/calendar_local_report_views.xml",
    ],
    "application": False,
    "installable": True,
}