from odoo import models, fields, api, _
import datetime
from odoo.tools.safe_eval import safe_eval


class PartnerEvent(models.Model):
    _name = 'partner.event'
    _description = 'Customer Dialogue'
    _inherit = ['mail.thread']

    name = fields.Char(string="Event Segment")
    organizer_id = fields.Many2one('res.partner', string="Organizer")
    is_online = fields.Boolean('Online Event')
    address_id = fields.Many2one(
        'res.partner', string='Location',
        default=lambda self: self.env.user.company_id.partner_id,
        readonly=False, states={'done': [('readonly', True)]},
        track_visibility="onchange")
    country_id = fields.Many2one('res.country', 'Country', related='address_id.country_id', store=True, readonly=False)
    category = fields.Char(string="Category")
    user_id = fields.Many2one('res.users', string="Responsible", default=lambda self: self.env.user.id)
    date_begin = fields.Datetime(string="Start Date", required=True)
    date_end = fields.Datetime(string="End Date", required=True)

    @api.model
    def _prefill_email_schedule_ids(self):
        values = [
            (0, 0, {
                'template_id': self.env.ref('af_automatic_customer_dialogue.on_boarding_email_template'),
                'interval_type': 'after_sub',
                'interval_nbr': 1,
                'interval_unit': 'now'
            }),
            (0, 0, {
                'template_id': self.env.ref('af_automatic_customer_dialogue.meeting_reminder_email_template'),
                'interval_type': 'before_event',
                'interval_nbr': 1,
                'interval_unit': 'days'
            }),
            (0, 0, {
                'template_id': self.env.ref('af_automatic_customer_dialogue.meeting_follow_up_email_template'),
                'interval_type': 'after_event',
                'interval_nbr': 3,
                'interval_unit': 'days'
            })]
        return values

    email_schedule_ids = fields.One2many('partner.event.email.schedule', 'partner_event_id',
                                         string="Email Schedule", default=_prefill_email_schedule_ids)

    state = fields.Selection([('draft', 'Draft'), ('running', 'Running'), ('canceled', 'Cancelled')], default='draft')
    color = fields.Integer('Kanban Color Index')

    @api.model
    def _get_daily_partner(self):
        daily_notes = self.env['res.partner.notes'].search([('note_type.name', '=', '90'),
                                                            ('partner_id.segment_jobseeker', '=', 'a')])
        return [("notes_ids", "in", daily_notes.ids)]

    contact_domain = fields.Char(string="Search Filter", default=_get_daily_partner)

    def automated_event_mail(self):
        event_ids = self.env['partner.event'].search([('state', '=', 'running')])
        for record in event_ids:
            for rec in record.email_schedule_ids:
                if rec.interval_type == 'after_sub' and not rec.sent:
                    self.after_registration(record, rec)
                if rec.interval_type == 'before_event' and not rec.sent:
                    self.before_event(record, rec)
                if rec.interval_type == 'after_event' and not rec.sent:
                    self.after_event(record, rec)

    def after_registration(self, event_id, event_mail_id):
        today_date = datetime.datetime.today().strftime("%Y-%m-%d")
        if event_mail_id.interval_unit == 'now':
            self.email_to_contacts(event_id, event_mail_id)
        elif event_mail_id.interval_unit == 'hours':
            _datetime = event_id.create_date + datetime.timedelta(hours=event_mail_id.interval_nbr)
            _date = _datetime.strftime("%Y-%m-%d %H")
            if _date == datetime.datetime.today().strftime("%Y-%m-%d %H"):
                self.email_to_contacts(event_id, event_mail_id)
        elif event_mail_id.interval_unit == 'days':
            _datetime = event_id.create_date + datetime.timedelta(days=event_mail_id.interval_nbr)
            _date = _datetime.strftime("%Y-%m-%d")
            if _date == today_date:
                self.email_to_contacts(event_id, event_mail_id)
        elif event_mail_id.interval_unit == 'weeks':
            _datetime = event_id.create_date + datetime.timedelta(weeks=event_mail_id.interval_nbr)
            _date = _datetime.strftime("%Y-%m-%d")
            if _date == today_date:
                self.email_to_contacts(event_id, event_mail_id)

    def before_event(self, event_id, event_mail_id):
        today_date = datetime.datetime.today().strftime("%Y-%m-%d")
        if event_mail_id.interval_unit == 'now':
            self.email_to_contacts(event_id, event_mail_id)
        elif event_mail_id.interval_unit == 'hours':
            _datetime = event_id.date_begin - datetime.timedelta(hours=event_mail_id.interval_nbr)
            _date = _datetime.strftime("%Y-%m-%d %H")
            if _date == datetime.datetime.today().strftime("%Y-%m-%d %H"):
                self.email_to_contacts(event_id, event_mail_id)
        elif event_mail_id.interval_unit == 'days':
            _datetime = event_id.date_begin - datetime.timedelta(days=event_mail_id.interval_nbr)
            _date = _datetime.strftime("%Y-%m-%d")
            if _date == today_date:
                self.email_to_contacts(event_id, event_mail_id)
        elif event_mail_id.interval_unit == 'weeks':
            _datetime = event_id.date_begin - datetime.timedelta(weeks=event_mail_id.interval_nbr)
            _date = _datetime.strftime("%Y-%m-%d")
            if _date == today_date:
                self.email_to_contacts(event_id, event_mail_id)

    def after_event(self, event_id, event_mail_id):
        today_date = datetime.datetime.today().strftime("%Y-%m-%d")
        if event_mail_id.interval_unit == 'now':
            self.email_to_contacts(event_id, event_mail_id)
        elif event_mail_id.interval_unit == 'hours':
            _datetime = event_id.date_end + datetime.timedelta(hours=event_mail_id.interval_nbr)
            _date = _datetime.strftime("%Y-%m-%d %H")
            if _date == datetime.datetime.today().strftime("%Y-%m-%d %H"):
                self.email_to_contacts(event_id, event_mail_id)
        elif event_mail_id.interval_unit == 'days':
            _datetime = event_id.date_end + datetime.timedelta(days=event_mail_id.interval_nbr)
            _date = _datetime.strftime("%Y-%m-%d")
            if _date == today_date:
                self.email_to_contacts(event_id, event_mail_id)
        elif event_mail_id.interval_unit == 'weeks':
            _datetime = event_id.date_end + datetime.timedelta(weeks=event_mail_id.interval_nbr)
            _date = _datetime.strftime("%Y-%m-%d")
            if _date == today_date:
                self.email_to_contacts(event_id, event_mail_id)

    def email_to_contacts(self, event_id, event_mail_id):
        domain = safe_eval(event_id.contact_domain)
        res_ids = self.env['res.partner'].search(domain).ids
        for rec in res_ids:
            partner_id = self.env['res.partner'].search([('id', '=', rec)])
            event_mail_id.template_id.with_context(
                partner_email=partner_id.email, partner_lang=partner_id.lang
            ).send_mail(event_id.id, force_send=True)
        event_mail_id.sent = True

    def start_event(self):
        self.state = 'running'

    def button_cancel(self):
        self.state = 'canceled'


class EventEmailSchedule(models.Model):
    _name = 'partner.event.email.schedule'

    name = fields.Text(string='Description')
    template_id = fields.Many2one('mail.template', string="Email Template")

    partner_event_id = fields.Many2one('partner.event', string="Partner Event")

    interval_nbr = fields.Integer('Interval', default=1)
    interval_unit = fields.Selection([
        ('now', 'Immediately'),
        ('hours', 'Hour(s)'), ('days', 'Day(s)'),
        ('weeks', 'Week(s)'), ('months', 'Month(s)')],
        string='Unit', default='hours', required=True)
    interval_type = fields.Selection([
        ('after_sub', 'After each registration'),
        ('before_event', 'Before the event'),
        ('after_event', 'After the event')],
        string='Trigger ', default="before_event", required=True)

    sent = fields.Boolean('Sent', readonly=True)
