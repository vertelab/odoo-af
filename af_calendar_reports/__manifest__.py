# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "AF Calendar Report",
    "version": "12.0.1.3",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "description": """
	 This module adds a template for sending meeting confirmations to the participants. 
	 v12.0.1.3 KPD-516 - Change sortorder in Meetings-tab
    """,
    "depends": ["calendar_af"],
    "external_dependencies": [],
    "data": [
        'views/calendar_appointment.xml',
        'views/appointment_report.xml',
        'views/updated_appointment_report.xml',
        'views/cancelled_appointment_report.xml',
        'data/mail_template.xml',
        'data/mail_template_users.xml',

    ],
    "application": True,
    "installable": False,
}
