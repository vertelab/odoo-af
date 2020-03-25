# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from ast import literal_eval


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    encrypted_vault_password_length = fields.Integer(
        string="Password length",
    )
    encrypted_vault_use_digits = fields.Boolean(
        string="Use Digits",
    )
    encrypted_vault_use_letters = fields.Boolean(
        string="Use Letters",
    )
    encrypted_vault_use_special = fields.Boolean(
        string="Use Special Characters",
        help="Those characters include: !@#$%^&*()="
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            encrypted_vault_password_length=literal_eval(
                get_param('encrypted_vault.encrypted_vault_password_length')),
            encrypted_vault_use_digits=literal_eval(
                get_param('encrypted_vault.encrypted_vault_use_digits')),
            encrypted_vault_use_letters=literal_eval(
                get_param('encrypted_vault.encrypted_vault_use_letters')),
            encrypted_vault_use_special=literal_eval(
                get_param('encrypted_vault.encrypted_vault_use_special')),
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param(
            'encrypted_vault.encrypted_vault_password_length',
            repr(self.encrypted_vault_password_length)
        )
        set_param(
            'encrypted_vault.encrypted_vault_use_digits',
            repr(self.encrypted_vault_use_digits)
        )
        set_param(
            'encrypted_vault.encrypted_vault_use_letters',
            repr(self.encrypted_vault_use_letters)
        )
        set_param(
            'encrypted_vault.encrypted_vault_use_special',
            repr(self.encrypted_vault_use_special)
        )
