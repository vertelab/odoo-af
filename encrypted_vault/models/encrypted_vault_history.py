# Copyright 2017 - 2018 Modoolar <info@modoolar.com>
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

from odoo import models, fields, api


class EncryptedVaultHistory(models.Model):
    _name = 'encrypted.vault.history'
    _order = 'create_date desc'

    encrypted_data = fields.Encrypted()

    name = fields.Char(
        string="Name",
        related="vault_id.name",
    )
    username = fields.Char(
        string="Username",
        required=True,
        encrypt="encrypted_data",
    )
    password = fields.Char(
        string="Password",
        required=True,
        encrypt="encrypted_data",
    )
    uri = fields.Char(
        string="URI",
        required=True,
        encrypt="encrypted_data",
    )
    create_date = fields.Datetime(
        comodel_name='Create Date',
        readonly=True
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Modified by',
        readonly=True,
    )

    vault_id = fields.Many2one(
        comodel_name="encrypted.vault",
        string="Vault",
        required=True,
        ondelete="cascade",
    )

    @api.multi
    def restore(self):
        self.ensure_one()
        self.vault_id.write({
            'username': self.username,
            'password': self.password,
            'uri': self.uri,
        })
