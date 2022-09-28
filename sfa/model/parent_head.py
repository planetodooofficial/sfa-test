from odoo import fields, api, models, _


class ParentHead(models.Model):
    _name = 'parent.head'
    _rec_name = 'name'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")