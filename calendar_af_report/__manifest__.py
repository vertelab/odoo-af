# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Calendar management - AF Reports",
    "version": "12.0.1.0.0",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "summary": "Calendar management - reports",
    "description": """ """,
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
