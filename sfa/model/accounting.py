from odoo import fields, models, api, _


class InheritAccountMove(models.Model):
    _inherit = 'account.move'

    voucher_type = fields.Char('Voucher Type')
