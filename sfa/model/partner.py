from odoo import fields, api, models


class InheritPartner(models.Model):
    _inherit = 'res.partner'

    pan_no = fields.Char('Pan')
