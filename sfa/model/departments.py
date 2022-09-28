from odoo import fields, api, models


class DepartmentsCenter(models.Model):
    _name = 'departments.center'
    _rec_name = 'name'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")


class SubDepartments(models.Model):
    _name = 'sub.departments'
    _rec_name = 'name'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
