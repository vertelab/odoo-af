from odoo import models, fields, api
import datetime


class PartnerNotes(models.Model):
    _inherit = 'res.partner.notes'

    @api.model
    def create(self, vals):
        today_date = datetime.datetime.today().strftime("%Y-%m-%d")
        res = super(PartnerNotes, self).create(vals)
        if vals.get('partner_id'):
            partner_rec = self.env['res.partner'].search([('id', '=', vals.get('partner_id'))])
            if partner_rec:
                if vals.get('note_type'):
                    partner_note_rec = self.env['res.partner.note.type'].search([('id', '=', vals.get('note_type'))])
                    if partner_note_rec:
                        if (vals.get('note_date') == today_date) and (partner_note_rec.name == '90') and (
                                partner_rec.segment_jobseeker == 'a'):
                            template_id = self.env.ref('af_automatic_customer_dialogue.on_boarding_email_template')
                            template_id.sudo().with_context(
                                partner_email=partner_rec.email, partner_lang=partner_rec.lang
                            ).send_mail(self.id, force_send=True)
        return res
