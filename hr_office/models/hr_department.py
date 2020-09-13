from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


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
