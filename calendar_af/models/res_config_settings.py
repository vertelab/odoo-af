# -*- coding: utf-8 -*-

from odoo import api, fields, models
import os

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Set start date for booking meeting
    af_start_meeting_search = fields.Char(string='Start Meeting Search',help="Set number of days from today a free meeting is searchable")
    af_stop_meeting_search = fields.Char(string='Stop Meeting Search',help="Set number of days from searchable parameter that a meeting is searchable")

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





