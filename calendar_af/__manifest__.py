# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Calendar management - AF",
    "version": "12.0.1.0.5",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "summary": "12.0.1.0.3 -AFC-1031 - Lägg till Helger och röda dagar i Resource Leaves.",
    "description": """
Description
================================================================================================
Asök booking management \n
12.0.1.0.3 - AFC-1046 - Lägg till Helger och röda dagar i Resource Leaves.\n
    """,
    "depends": [
        "calendar",
        "contacts",
        "af_security",
        "hr_skill",
        'hr',
    ],
    "external_dependencies": [
    ],
    "data": [
        "data/calendar.channel.csv",
        "data/calendar.appointment.type.csv",
        "data/calendar.appointment.cancel_reason.csv",
        "data/resource.calendar.leaves.csv",
        "data/mail_template.xml",
        "data/calendar_schedule_cron.xml",
        "security/ir.model.access.csv",
        "views/hr_location_view.xml",
        "views/res_users_view.xml",
        "views/calendar_af_view.xml",
        "views/calendar_schedule_view.xml",
        "views/calendar_appointment_view.xml",
        "views/calendar_occasion_view.xml",
        "views/calendar_channel_view.xml",
        "views/calendar_appointment_type_view.xml",
        "views/calendar_mapped_dates_view.xml",
        "wizard/cancel_appointment.xml",
        "wizard/create_local_occasion.xml",
        "report/calendar_report_views.xml",
        "report/calendar_local_report_views.xml",
    ],
    "application": True,
    "installable": True,
}
