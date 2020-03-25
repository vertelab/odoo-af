# Copyright 2017 - 2018 Modoolar <info@modoolar.com>
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

import logging
from random import choice
from ast import literal_eval
from string import digits, ascii_letters
from odoo import models, fields, api

_logger = logging.getLogger(__name__)
try:
    fields.Encrypted
except AttributeError:
    _logger.fatal("\n\n===================================================\n\n"
                  "Encrypted field does not exist!\nCheck if "
                  "base_encrypted_field is added to server_wide_modules "
                  "config parameter.\n\n"
                  "===================================================\n\n")


class EncryptedVault(models.Model):
    _name = 'encrypted.vault'

    @api.model
    def random_password(self, pass_len=False):
        get_param = self.env['ir.config_parameter'].sudo().get_param
        pass_len = pass_len if pass_len else literal_eval(get_param(
            'encrypted_vault.encrypted_vault_password_length'))
        characters = ""
        use_digits = literal_eval(
            get_param('encrypted_vault.encrypted_vault_use_digits'))
        use_letters = literal_eval(
            get_param('encrypted_vault.encrypted_vault_use_letters'))
        use_special = literal_eval(
            get_param('encrypted_vault.encrypted_vault_use_special'))
        if use_digits:
            characters += digits
        if use_special:
            characters += "!@#$%^&*()="
        if use_letters:
            characters += ascii_letters
        if not characters:
            characters += ascii_letters + digits
        password = ''.join(choice(characters) for x in range(pass_len))
        return password

    encrypted_data = fields.Encrypted()
    name = fields.Char(
        required=True,
    )
    username = fields.Char(
        required=False,
    )
    password = fields.Char(
        required=False,
        encrypt="encrypted_data",
        default=random_password
    )
    uri = fields.Char(
        string="URI",
        required=False,
    )
    notes = fields.Text(
        encrypt="encrypted_data",
    )

    # This will be implemented in future.
    # uri_ids = fields.One2many(
    #     comodel_name="encrypted.vault.uri",
    #     inverse_name="vault_id",
    #     string="URIs",
    #     required=False,
    # )

    history_ids = fields.One2many(
        comodel_name="encrypted.vault.history",
        inverse_name="vault_id",
        string="History",
        required=False,
    )

    history_count = fields.Integer(
        compute='_compute_history_count',
    )
    custom_field_ids = fields.One2many(
        comodel_name="encrypted.vault.custom.field",
        inverse_name="vault_id",
        string="Custom Fields",
        required=False,
        copy=True,
    )

    @api.multi
    def _compute_history_count(self):
        for vault in self:
            vault.history_count = len(vault.history_ids)

    @api.multi
    def write(self, vals):
        if any(key in vals for key in self.get_history_fields()):
            for record in self:
                self.env["encrypted.vault.history"].sudo() \
                    .create(self.prepare_history_vals(record))
        return super(EncryptedVault, self).write(vals)

    @api.model
    def get_history_fields(self):
        return ["username", "password", "uri"]

    @api.model
    def prepare_history_vals(self, record):
        return {
            "user_id": self.env.uid,
            "vault_id": record.id,
            "username": record.username,
            "password": record.password,
            "uri": record.uri,
        }

    @api.multi
    def random_password_button(self):
        self.ensure_one()
        self.password = self.random_password()
