# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2019 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    kpi_ids = fields.One2many(comodel_name="res.partner.kpi", inverse_name="partner_id")


class ResPartnerKpi(models.Model):
    _name = "res.partner.kpi"
    _description = "RES Partner KPI"

    partner_id = fields.Many2one(comodel_name="res.partner")
    # name = fields.Char(string="", help="", required=True)
    fiscal_year = fields.Datetime(string="Fiscal year")
    turnover = fields.Integer(string="Turnover")
    turnover_change = fields.Integer(compute="compute_change", store=True)
    turnover_change_percent = fields.Integer(compute="compute_turnover_change_percent", store=True)
    profit = fields.Integer(string="Profit")
    profit_percent = fields.Integer(compute="compute_profit_percent", store=True)
    profit_change = fields.Integer(compute="compute_change", store=True)
    profit_change_percent = fields.Integer(compute="compute_profit_change_percent", store=True)
    employees = fields.Integer(string="Employees")
    employees_change = fields.Integer(compute="compute_change", store=True)
    employees_change_percent = fields.Integer(compute="compute_employees_change_percent", store=True)
    size = fields.Selection(selection=[
        ('1', 'Class 1'),
        ('2', 'Class 2'),
        ('3', 'Class 3'),
        ('4', 'Class 4'),
        ('5', 'Class 5'),
        ('6', 'Class 6'),
        ('7', 'Class 7'),
        ('8', 'Class 8'),
        ('9', 'Class 9')],
        string='Size class',
        default='1',
        help="Size class")

    @api.one
    @api.depends('profit', 'turnover')
    def compute_profit_percent(self):
        if self.turnover != 0:
            decimal = (float(self.profit) / self.turnover)
            if decimal > 1:
                decimal = decimal - 1
            else:
                decimal = 1 - decimal
                decimal = decimal * -1

            decimal = decimal * 100
            decimal = round(decimal, 0)
            self.profit_percent = int(decimal)

    @api.one
    @api.depends('profit', 'turnover', 'employees')
    def compute_change(self):
        previous = self.env['res.partner.kpi'].search([('fiscal_year', '<', self.fiscal_year)],
                                                      order='fiscal_year DESC', limit=1)
        if previous:
            self.turnover_change = self.turnover - previous.turnover
            self.profit_change = self.profit - previous.profit
            self.employees_change = self.employees - previous.employees
        else:
            self.turnover_change = 0
            self.profit_change = 0
            self.employees_change = 0

    # @api.one
    # def compute_profit_change(self):
    #    previous = self.env['res.partner.kpi'].search([('fiscal_year', '<', self.fiscal_year)], order='fiscal_year DESC', limit=1)
    #    self.profit_change = self.profit - previous.profit
    # @api.one
    # def compute_employees_change(self):
    #    previous = self.env['res.partner.kpi'].search([('fiscal_year', '<', self.fiscal_year)], order='fiscal_year DESC', limit=1)
    #    self.employees_change = self.employees - previous.employees

    @api.one
    @api.depends('turnover')
    def compute_turnover_change_percent(self):
        previous = self.env['res.partner.kpi'].search([('fiscal_year', '<', self.fiscal_year)],
                                                      order='fiscal_year DESC', limit=1)
        if not previous:
            self.turnover_change_percent = 0
        elif previous.turnover != 0:
            decimal = (float(self.turnover - previous.turnover) / previous.turnover)
            decimal = decimal * 100
            decimal = round(decimal, 0)
            self.turnover_change_percent = int(decimal)

    @api.one
    @api.depends('profit')
    def compute_profit_change_percent(self):
        previous = self.env['res.partner.kpi'].search([('fiscal_year', '<', self.fiscal_year)],
                                                      order='fiscal_year DESC', limit=1)
        if not previous:
            self.profit_change_percent = 0
        elif previous.profit != 0:
            decimal = (float(self.profit - previous.profit) / previous.profit)
            decimal = decimal * 100
            decimal = round(decimal, 0)
            self.profit_change_percent = int(decimal)

    @api.one
    @api.depends('employees')
    def compute_employees_change_percent(self):
        previous = self.env['res.partner.kpi'].search([('fiscal_year', '<', self.fiscal_year)],
                                                      order='fiscal_year DESC', limit=1)
        if not previous:
            self.employees_change_percent = 0
        elif previous.employees != 0:
            decimal = (float(self.employees - previous.employees) / previous.employees)
            decimal = decimal * 100
            decimal = round(decimal, 0)
            self.employees_change_percent = int(decimal)
