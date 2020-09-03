# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "AF Calendar Report",
    "version": "12.0.1.0.1",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "depends": ["calendar_af"],
    "external_dependencies": [],
    "data": [
        'views/appointment_report.xml',
        'views/updated_appointment_report.xml',
        'data/mail_template.xml',

    ],
    "application": True,
    "installable": True,
}
