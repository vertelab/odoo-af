# Copyright 2017 - 2018 Modoolar <info@modoolar.com>
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

from odoo import models, fields, api

FIELD_TYPES = [
    ('hidden', 'Hidden'),
    ('text', 'Text'),
    ('boolean', 'Boolean'),
]


class EncryptedVaultCustomField(models.Model):
    _name = 'encrypted.vault.custom.field'

    encrypted_data = fields.Encrypted()
    name = fields.Char(
        string="Name",
        required=True,
        encrypt="encrypted_data",
    )

    type = fields.Selection(
        selection=FIELD_TYPES,
        string="Type",
        default='text',
        required=True,
        encrypt="encrypted_data"
    )
    vault_id = fields.Many2one(
        comodel_name="encrypted.vault",
        string="Vault",
        required=True,
        ondelete="cascade",
    )

    text = fields.Char(
        string="Value",
        encrypt="encrypted_data"
    )
    hidden = fields.Char(
        string="Value",
        encrypt="encrypted_data"
    )
    boolean = fields.Boolean(
        string="Value",
        encrypt="encrypted_data"
    )

    @api.onchange("type")
    def _on_type_change(self):
        for record in self:
            if not record.type:
                continue
            for t in FIELD_TYPES:
                if record.type != t[0]:
                    record[record.type] = False
