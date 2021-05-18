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
    "version": "12.0.3.1.4",
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
        "wizard/move_appointment.xml",
    ],
    "application": True,
    "installable": True,
}
