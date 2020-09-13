from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class HR(models.Model):
    _inherit = 'hr.employee'

    related_partner_id = fields.Many2one('res.partner', string="Related Partner", related='user_id.partner_id')
    jobseekers_ids = fields.One2many('res.partner', compute='_get_records')
    case_ids = fields.One2many('res.partner.case', compute='_get_records')
    daily_note_ids = fields.One2many('res.partner.notes', compute='_get_records')

    @api.depends('user_id')
    def _get_records(self):
        for rec in self:
            if rec.user_id:
                rec.jobseekers_ids = rec.env['res.partner'].search([('user_id', '=', rec.user_id.id)])
                rec.case_ids = rec.env['res.partner.case'].search([('administrative_officer', '=', rec.user_id.id)])
                rec.daily_note_ids = rec.env['res.partner.notes'].search([('administrative_officer', '=', rec.user_id.id)])

    @api.multi
    def search_jobseeker_action(self):
        return {
            'res_model': 'hr.employee',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('hr_360_view.search_jobseeker_form').id,
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {},
        }

class HrDepartment(models.Model):
    _inherit = "hr.department"

    office_code = fields.Char(string="Office code")


class HrCampus(models.Model):
    _name = "hr.campus"

    name = fields.Char(string="Name")
    opening_hours = fields.Char(string = 'Opening hours')
    personal_service_opening = fields.Char(string="Opening hours for personal service")
    location_code = fields.Char(string="Location code")
    
    public_contact = fields.Many2one('hr.employee', string="Public contact")
    office_id = fields.Many2many(comodel_name='hr.department', string="Office")
    partner_id = fields.Many2one('res.partner', string="Partner") # for fields like fax, phone etc
    visitation_address_id = fields.Many2one('res.partner', string="Visitation address")
    mailing_address_id = fields.Many2one('res.partner', string="Mailing address")
    
    office_code = fields.Char(string="Office code", related="office_id.office_code")
    
    accesibilities = fields.Many2many(comodel_name='hr.campus.accessibilities', string="Accessibilities")

class HrCampusAccessibilities(models.Model):
    _name = "hr.campus.accessibilities"

    name= fields.Char(string="Type")
    description = fields.Char(string="Description")
    
# [{
#     "active": "true",
#     "name": "Af Karlskrona",
#     "office_code": "1020",
#     "personal_service_opening": "måndag-fredag 10-16",
#     "phone_hours": "Växeln är öppen måndag-fredag 8-16.30",
#     "opening_hours": "måndag-fredag 10-16",
#     "fax_number": "0104860100",
#     "email_address": "karlskrona@arbetsformedlingen.se",
#     "phone_number": "0771600000",
#     "organisational_belonging": "Mo Småland Blekinge Chef Sektion 1 21000001",
#     "organisational_belonging.u_copakod": "a21b00c00d01",
#     "operation_id": "0000001155",
#     "last_operation_day": null,
#     "public_contact": "Conny Olausson (olaco)",
#     "public_contact.source": "ldap:cn=olaco,ou=Users,o=AF,c=SE",
#     "public_contact.user_name": "olaco",
#     "visiting_address.street": "Östra Köpmansgatan 31",
#     "visiting_address.zip": "371 32",
#     "visiting_address.city": "Karlskrona",
#     "mailing_address.street": "Box 306",
#     "mailing_address.zip": "371 25",
#     "mailing_address.city": "Karlskrona",
#     "campus.name": "Karlskrona, Östra Köpmansgatan 31",
#     "campus.workplace_number": "1020",
#     "campus.location_code": "71020",
#     "campus.county_number": "10",
#     "campus.latitude": "56.1638",
#     "campus.longitude": "15.5873",
#     "x500_id": "12345552",
#     "accessibilities": [{
#         "type": "Rörelsehinder",
#         "description": "Du kan ta dig från entrén till informationsdisken, kapprummet och toaletten utan att passera trappsteg, om ramp eller hiss saknas."
#       },
#       {
#         "type": "Rörelsehinder",
#         "description": "Entrédörren har en dörröppnare."
#       }
#     ]
#   },