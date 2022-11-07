from num2words import num2words
from odoo import fields, api, models, _
import time
from odoo.exceptions import UserError, ValidationError

class InheritPaySlip(models.Model):
    _inherit = 'hr.payslip'

    # days = fields.Integer(compute='_attendance', string='amt')

    def _compute_total_claimable_amt_words(self, amount):
        return self.currency_id.amount_to_text(amount)

