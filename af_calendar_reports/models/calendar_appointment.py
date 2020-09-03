from odoo import models, api, _, fields
from  datetime import datetime


class CalendarAppointment(models.Model):
    _inherit = 'calendar.appointment'

    @api.model
    def create(self, vals):
        res = super(CalendarAppointment, self).create(vals)
        template = self.env.ref('af_calendar_reports.email_template_calendar_appointment')
        self.env['mail.template'].browse(template.id).send_mail(res.id, force_send=True)
        return res

    @api.multi
    def write(self, vals):
        template = self.env.ref('af_calendar_reports.email_template_updated_calendar_appointment')
        self.env['mail.template'].browse(template.id).send_mail(self.id, force_send=True)
        return super(CalendarAppointment, self).write(vals)


class CancelAppointment(models.TransientModel):
    _inherit = 'calendar.cancel_appointment'
    _description = 'Cancel appointment'

    def action_cancel_appointment(self):
        if self.cancel_reason:
            template = self.env.ref('af_calendar_reports.email_template_cancelled_calendar_appointment')
            self.env['mail.template'].browse(template.id).send_mail(self.id, force_send=True)
            return self.appointment_ids.cancel(self.cancel_reason)
