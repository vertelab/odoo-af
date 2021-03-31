# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Calendar management - AF",
    "version": "12.0.3.0.0",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "summary": "Calendar management",
    'description': """
Module for AF appointments
================================================================================================
This module adds new functionality regarding appointments functionality \n
This functionality is tailored for AF. \n
v12.0.1.0.7: versions before good version control \n
v12.0.1.0.8 AFC-1771: added sort order for calendar.appointment.type \n
v12.0.1.0.9 AFC-1908: changed type_id Many2one to show 15 entries before showing "search more" option. \n
v12.0.2.0.0 AFC-1805: Major overhaul of functionality. PDM occasions now handled differently. \n
v12.0.3.0.0 AFC-2044: Major overhaul of functionality. All occasions now handled differently. \n
\n
""",
    "depends": [
        "calendar",
        "contacts",
        "af_security",
        "hr_skill",
        "hr_office",
        "web_m2x_options"
    ],
    "external_dependencies": [
    ],
    "data": [
        "data/calendar.channel.csv",
        "data/calendar.appointment.type.csv",
        "data/calendar.appointment.cancel_reason.csv",
        "data/mail_template.xml",
        "data/calendar_schedule_cron.xml",
        "security/ir.model.access.csv",
        "views/hr_operation_view.xml",
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
        "wizard/change_user_appointment.xml",
    ],
    "application": True,
    "installable": True,
}
