# -*- coding: utf-8 -*-

from odoo import api, fields, models
import os

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # address
    af_ipf_url = fields.Char(string='IPF API URL',help="If you need help you shouldn't be changing this")
    af_ipf_port = fields.Char(string='IPF API port',help="If you need help you shouldn't be changing this")
    # id and secret
    af_client_id = fields.Char(string='Client Id',help="If you need help you shouldn't be changing this")
    af_client_secret = fields.Char(string='Client secret',help="If you need help you shouldn't be changing this")
    # headers
    af_environment = fields.Char(string='AF-Environment',help="If you need help you shouldn't be changing this")
    af_system_id = fields.Char(string='AF-SystemId',help="If you need help you shouldn't be changing this")
    # tracking_id is a unique id for each transaction. Not a good parameter to set.
    # af_tracking_id = fields.Char(string='AF-TrackingId',help="If you need help you shouldn't be changing this")
        
    @api.model
    def get_values(self):
        res = super().get_values()

        af_env = os.environ['AFENVIRONMENT']
        af_ipfport = os.environ['AFIPFPORT']
        af_ipfurl = os.environ['AFIPFURL']

        get_param = self.env['ir.config_parameter'].sudo().get_param
        
        res.update({
            'af_client_id': get_param('af_rest.client_id'),
            'af_client_secret': get_param('af_rest.client_secret'),
            'af_environment': af_env if af_env else get_param('af_rest.af_environment') ,
            'af_ipf_port': af_ipfport if af_ipfport else get_param('af_rest.ipf_port') ,
            'af_ipf_url': af_ipfurl if af_ipfurl else get_param('af_rest.ipf_url') ,
            'af_system_id': get_param('af_rest.af_system_id'),
            # 'af_tracking_id': get_param('af_rest.af_tracking_id'),
        })
        return res

    @api.multi
    def set_values(self):
        super().set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('af_rest.client_id', self.af_client_id)
        set_param('af_rest.client_secret', self.af_client_secret)
        set_param('af_rest.af_environment', self.af_environment)
        set_param('af_rest.ipf_port', self.af_environment)
        set_param('af_rest.ipf_url', self.af_environment)
        set_param('af_rest.af_system_id', self.af_system_id)




