from odoo import models, api, _, fields
from datetime import datetime


class CalendarAppointment(models.Model):
    _inherit = 'calendar.appointment'

    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.user.company_id)

    @api.model
    def create(self, vals):
        res = super(CalendarAppointment, self).create(vals)
        template = self.env.ref(
            'af_calendar_reports.email_template_calendar_appointment')
        template.send_mail(res.id, force_send=True)
        return res

    @api.multi
    def write(self, vals):
        res = super(CalendarAppointment, self).write(vals)
        template = self.env.ref(
            'af_calendar_reports.email_template_updated_calendar_appointment')
        # There should probably be a check here to see if this is needed, or we
        # risk spamming the recipient.
        for appointment in self:
            template.send_mail(appointment.id, force_send=True)
        return res


class CancelAppointment(models.TransientModel):
    _inherit = 'calendar.cancel_appointment'
    _description = 'Cancel appointment'

    def action_cancel_appointment(self):
        if self.cancel_reason:
            template = self.env.ref(
                'af_calendar_reports.email_template_cancelled_calendar_appointment')
            for appointment in self.appointment_ids:
                template.send_mail(appointment.id, force_send=True)
        return self.appointment_ids.cancel(self.cancel_reason)
