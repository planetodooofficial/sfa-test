import fiscalyear
from odoo import models, fields, api


class TaxDeclareCustom(models.Model):
    _inherit = "hr.employee"

    emp_tax_dec_ids = fields.One2many('employee.tax.declaration', 'name', 'Employee Tax Declaration Ids')

