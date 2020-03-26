# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Calendar AF",
    "version": "12.0.1.0.0",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": ["calendar", ],
    "external_dependencies": [
        # "service_identity",
        # "stompest",
        # "stompest.async",
    ],
    "data": [
        "views/calendar_schedule_view.xml",
        "views/calendar_appointment_view.xml",
        "security/ir.model.access.csv",
        "data/calendar.schedule.competence.csv",
    ],
    "application": True,
    "installable": True,
}
