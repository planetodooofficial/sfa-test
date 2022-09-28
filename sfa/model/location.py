from odoo import fields, api, models, _


class LocationCenter(models.Model):
    _name = 'location.center'
    _rec_name = 'name'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")