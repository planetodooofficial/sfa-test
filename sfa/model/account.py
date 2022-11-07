from odoo import fields, api, models, _
import json
from num2words import num2words


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    total_igst_amt = fields.Float(compute='calculate_tax')
    total_sgst_amt = fields.Float(compute='calculate_tax')
    total_cgst_amt = fields.Float(compute='calculate_tax')
    amt = fields.Char(string="Amount", compute='amt_in_words')

    def amt_in_words(self):
        self.amt = num2words(str(round(self.amount_total, 0)), lang='en_IN').replace('and', '').replace('point', 'and').replace('thous', 'thousand')

    def calculate_tax(self):
        gst_value = {rec.get('tax_group_name'): rec.get('tax_group_amount') for rec in json.loads(self.tax_totals_json)['groups_by_subtotal']['Untaxed Amount']}
        self.total_igst_amt = gst_value.get('IGST') or ''
        self.total_sgst_amt = gst_value.get('SGST') or ''
        self.total_cgst_amt = gst_value.get('CGST') or ''
        # self.total_igst_amt = [rec.get('tax_group_amount') for rec in json.loads(self.tax_totals_json)['groups_by_subtotal']['Untaxed Amount'] if rec.get('tax_group_name', 'None') =='IGST' ][0] or ''
        # self.total_cgst_amt = [rec.get('tax_group_amount') for rec in json.loads(self.tax_totals_json)['groups_by_subtotal']['Untaxed Amount'] if rec.get('tax_group_name', 'None') =='CGST' ][0] or ''
        # self.total_sgst_amt = [rec.get('tax_group_amount') for rec in json.loads(self.tax_totals_json)['groups_by_subtotal']['Untaxed Amount'] if rec.get('tax_group_name', 'None') =='SGST' ][0] or ''


class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    hsn_code = fields.Char(string="HSN Code", related="product_id.l10n_in_hsn_code")


