from odoo import fields, api, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    pan_no = fields.Char(string='Pan')

