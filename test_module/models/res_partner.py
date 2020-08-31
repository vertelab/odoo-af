from odoo import models, fields, api, _
import logging

from odoo.exceptions import Warning


_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    test_char_field = fields.Char(string="Test Char field", help="this is a help text on a basic text field")
    test_float_field = fields.Float(string="Test Float field", help="Float field, usefull for time durations with the proper widget")
    test_integer_field = fields.Integer(string="Test Integer field", help="Integer field")
    test_datetime_field = fields.Datetime(string="Test Datetime field", help="Datetime field")
    test_selection_field = fields.Selection(string="Test Selection field", selection=[('item 1','Item 1'),('item 2','Item 2')], help="The first string in the touple is how the selection is identified, the second is the label that you see in the interface")
    test_model_ids = fields.Many2many(comodel_name="res.partner.test.model", string="Test Many2many relation field")
    test_related_field = fields.Char(string="Partner name", related="name", help="This field reflects the contents of the name field and is read only")
    test_model_m2o_id = fields.Many2one(string="Test Many2one relation field", comodel_name="res.partner.test.model_o2m", help="This is a Many2one field so you can only select one item")

    @api.multi
    def hello_world(self):
        _logger.info("hello world in the log!") #you can also use warn and error depending on the situation
        raise Warning('hello world!')

#these models require access rights to be set in an ir.model.access.csv file in order to work properly
class TestModel(models.Model):
    _name = "res.partner.test.model"

    partner_ids = fields.Many2many(comodel_name="res.partner", string="partners", help="You make lists (tree) of things by creating a many2one here and many2many on res.partner, thus allowing many things on one partner but only one per thing")

class TestModelM2O(models.Model):
    _name = "res.partner.test.model_o2m"

    partner_ids = fields.One2many(string="partners", comodel_name="res.partner", inverse_name="test_model_m2o_id", help="One2many relation requires inverse_name")
    

