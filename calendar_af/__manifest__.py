# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2021 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "Calendar management - AF",
    "version": "12.0.3.3.0",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "summary": "Calendar management",
    'description': """
Module for AF appointments \n
================================================================================================ \n
This module adds new functionality regarding appointments functionality \n
This functionality is tailored for AF. \n
v12.0.1.0.7: versions before good version control \n
v12.0.1.0.8 AFC-1771: added sort order for calendar.appointment.type \n
v12.0.1.0.9 AFC-1908: changed type_id Many2one to show 15 entries before showing "search more" option. \n
v12.0.2.0.0 AFC-1805: Major overhaul of functionality. PDM occasions now handled differently. \n
v12.0.3.0.0 AFC-2044: Major overhaul of functionality. All occasions now handled differently. \n
v12.0.3.0.1 AFC-1715: Added new appointment types and updated existing ones. \n
v12.0.3.0.2 AFC-2110: Removed raise Warnings to create better workflow. Added better filter after creating occasions. \n
v12.0.3.0.3 AFC-2113: Updated how res.users is presented in views. \n
v12.0.3.0.4 AFC-2168: Changed menu groups. \n
v12.0.3.1.0 AFC-2177: Reworked how appointments are rebooked. \n
v12.0.3.1.1 AFC-2229: Updated text on get new times buttons. \n
v12.0.3.1.2 AFC-2229: Removed duration selector when booking new appointment. \n
v12.0.3.1.3 AFC-2239: Fixed bug when booking meetings. \n
v12.0.3.1.4 AFC-2267: Fixed typo in code. \n
v12.0.3.1.4 AFC-2129: Re-added possibility to accept/reject/publish several occasions at once. \n
v12.0.3.1.5 AFC-2276: Changed access rights to models and changed views. \n
v12.0.3.1.6 AFC-2113: Updated view for local occasions. \n
v12.0.3.1.7 AFC-2303: Added support for operation_id in move-wizard. \n
v12.0.3.1.8 AFC-2278: Updated criteria for shown meetings. \n
v12.0.3.1.8 AFC-2293: Changed duration_text field to stored for calendar_occasion. \n
v12.0.3.1.9 AFC-2290: Changed duration_text field to stored for calendar_appointment. \n
v12.0.3.2.0 AFC-2335: Removed ability to open operation_ids from views. \n
v12.0.3.2.1 AFC-2328: Changed labels for create occasions view \n
v12.0.3.2.2 AFC-2334: Stopped regular users from editing employees on hr_operation \n
v12.0.3.2.3 AFC-2327: Fixed context when navigating views. \n
v12.0.3.3.0 AFC-2298: calendar_af: Fixed access rights and menus. \n
\n
""",
    "depends": [
        "calendar",
        "contacts",
        "af_security",
        "hr_skill",
        "hr_office",
        "web_m2x_options",
        "hr_holidays_leave_repeated",
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
        "views/hr_holidays_view.xml",
        "data/hr_holidays_data.xml",
        "wizard/cancel_appointment.xml",
        "wizard/create_local_occasion.xml",
        "wizard/change_user_appointment.xml",
        "wizard/move_appointment.xml",
    ],
    "application": True,
    "installable": True,
}
