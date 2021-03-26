# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
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

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Set start date for booking meeting
    af_start_meeting_search = fields.Char(string='Start Meeting Search',
                                          help="Set number of days from today a free meeting is searchable")
    af_stop_meeting_search = fields.Char(string='Stop Meeting Search',
                                         help="Set number of days from searchable parameter that a meeting is searchable")

    @api.model
    def get_values(self):
        res = super().get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update({
            'af_start_meeting_search': get_param('af_calendar.start_meeting_search'),
            'af_stop_meeting_search': get_param('af_calendar.stop_meeting_search'),
        })
        return res

    @api.multi
    def set_values(self):
        super().set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('af_calendar.start_meeting_search', self.af_start_meeting_search)
        set_param('af_calendar.stop_meeting_search', self.af_stop_meeting_search)
