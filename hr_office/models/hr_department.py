from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class HrDepartment(models.Model):
    _inherit = "hr.department"

    office_code = fields.Char(string="Office code") #fyrställig
    organisation_number = fields.Char(string="Organisaiton Number")
    operation_ids = fields.One2many(comodel_name='hr.campus', string="Campuses", inverse_name="office_id")
    


class HrOperation(models.Model):
    _name = "hr.operation"

    name = fields.Char(string="Name")
    opening_hours = fields.Char(string = 'Opening hours')
    personal_service_opening = fields.Char(string="Opening hours for personal service")
    
    #public_contact = fields.Many2one('hr.employee', string="Public contact")
    office_id = fields.Many2one(comodel_name='hr.department', string="Office")
    section_id = fields.Many2one(comodel_name='hr.department', string="Organisation") #ska ha section_id.parent_id = office_id
    partner_id = fields.Many2one('res.partner', string="Partner") 
    visitation_address_id = fields.Many2one('res.partner', string="Visitation address")
    mailing_address_id = fields.Many2one('res.partner', string="Mailing address")
    campus_id = fields.One2many('hr.campus', string="Campus")
    
    office_code = fields.Char(string="Office code", related="office_id.office_code")
    
    
    accessibilities = fields.Many2many(comodel_name='hr.operations.accessibilities', string="Accessibilities")


class HrCampus(models.Model):
    _name="hr.campus"

    workplace_number = fields.Char(string="Workplace number")
    location_code = fields.Char(string="Location code")
    visitation_address_id = fields.Many2one('res.partner', string="Visitation address")


class HrOperationAccessibilities(models.Model):
    _name = "hr.operation.accessibilities"

    name= fields.Char(string="Type")
    description = fields.Char(string="Description")
