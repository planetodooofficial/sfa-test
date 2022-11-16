from odoo import fields, models, api
from datetime import datetime
from odoo.exceptions import ValidationError
import json
from lxml import etree
from datetime import datetime


class AccountMoveInheritAdvance(models.Model):
    _inherit = "account.move"

    partial_lines = fields.One2many('partial.line', 'entry_id')
    pending_amt = fields.Float(compute="compute_pending_amt")
    custom_payment_type = fields.Selection([('inbound', 'Inbound'), ('outbound', 'outbound')])
    advance_ids = fields.One2many('advance.orders', 'move_id')
    is_advance = fields.Boolean(default=False, string="Advance?")
    adv_pending_amt = fields.Float(compute="compute_advance_pending_amt")

    @api.onchange('is_advance', 'partner_id')
    def unlink_advances(self):
        self.advance_ids.unlink()

    @api.depends("advance_ids.advance_amount")
    def compute_advance_pending_amt(self):
        amount = self.adv_pay_amt - sum(self.advance_ids.mapped('advance_amount'))
        if amount < 0:
            raise ValidationError('You are trying to assign advance amount more than the payment amount.')
        self.adv_pending_amt = amount

    @api.depends('partial_lines.amount')
    def compute_pending_amt(self):
        amount = self.adv_pay_amt - sum(self.partial_lines.mapped('amount'))
        if amount < 0:
            raise ValidationError('You are trying to reconcile more than the payment amount')
        self.pending_amt = amount

    def _get_valid_liquidity_accounts(self):
        return (
            self.journal_id.default_account_id.id,
            self.payment_method_line_id.payment_account_id.id,
            self.journal_id.company_id.account_journal_payment_debit_account_id.id,
            self.journal_id.company_id.account_journal_payment_credit_account_id.id,
            self.journal_id.inbound_payment_method_line_ids.payment_account_id.id,
            self.journal_id.outbound_payment_method_line_ids.payment_account_id.id,
        )

    @api.model
    def _get_default_currency(self):
        ''' Get the default currency from either the journal, either the default journal's company. '''
        journal = self._get_default_journal()
        return journal and (journal.currency_id or journal.company_id.currency_id) or False

    currency_id = fields.Many2one('res.currency', store=True, readonly=True, tracking=True, required=True,
                                  states={'draft': [('readonly', False)]},
                                  string='Currency',
                                  default=_get_default_currency)

    @api.model
    def _get_default_journal(self):
        res = super(AccountMoveInheritAdvance, self)._get_default_journal()
        if self._context.get('default_custom_payment_type'):
            return False
            # res = self.env['account.journal'].search([('type', '=', 'bank')])
        return res and res[0] or False

    journal_id = fields.Many2one('account.journal', string='Journal', required=True, readonly=True,
                                 states={'draft': [('readonly', False)]},
                                 check_company=True, domain="[('id', 'in', suitable_journal_ids)]",
                                 default=_get_default_journal)

    adv_pay_amt = fields.Float(string="Amount")
    payment_method_line_id = fields.Many2one('account.payment.method.line', string='Payment Method',
                                             readonly=False, store=True, copy=False,
                                             compute='_compute_payment_method_line_id',
                                             domain="[('id', 'in', available_payment_method_line_ids)]",
                                             help="Manual: Pay or Get paid by any method outside of Odoo.\n"
                                                  "Payment Acquirers: Each payment acquirer has its own Payment Method. Request a transaction on/to a card thanks to a payment token saved by the partner when buying or subscribing online.\n"
                                                  "Check: Pay bills by check and print it from Odoo.\n"
                                                  "Batch Deposit: Collect several customer checks at once generating and submitting a batch deposit to your bank. Module account_batch_payment is necessary.\n"
                                                  "SEPA Credit Transfer: Pay in the SEPA zone by submitting a SEPA Credit Transfer file to your bank. Module account_sepa is necessary.\n"
                                                  "SEPA Direct Debit: Get paid in the SEPA zone thanks to a mandate your partner will have granted to you. Module account_sepa is necessary.\n")
    available_payment_method_line_ids = fields.Many2many('account.payment.method.line',
                                                         compute='_compute_payment_method_line_fields')

    @api.onchange('journal_id', 'payment_method_line_id', 'adv_pay_amt')
    def create_move_line(self):
        os_line = self.line_ids.filtered(lambda x: x.is_os_line)
        if self.custom_payment_type == 'inbound' and self.payment_method_line_id:
            account_id = self.payment_method_line_id.payment_account_id or self.journal_id.company_id.account_journal_payment_debit_account_id
            if not os_line:
                self.line_ids = [(0, 0, {'account_id': account_id.id, 'debit': self.adv_pay_amt, 'is_os_line': True,
                                         'partner_id': self.partner_id.id})]
            else:
                self.update(dict(line_ids=[(1, os_line.id, {'account_id': account_id.id,
                                                            'debit': self.adv_pay_amt,
                                                            'partner_id': self.partner_id.id})]))
        elif self.custom_payment_type == 'outbound' and self.payment_method_line_id:
            account_id = self.payment_method_line_id.payment_account_id or self.journal_id.company_id.account_journal_payment_credit_account_id
            if not os_line:
                self.line_ids = [(0, 0, {'account_id': account_id.id, 'credit': self.adv_pay_amt, 'is_os_line': True,
                                         'partner_id': self.partner_id.id})]
            else:
                self.update(dict(line_ids=[(1, os_line.id, {'account_id': account_id.id, 'credit': self.adv_pay_amt,
                                                            'partner_id': self.partner_id.id})]))

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(AccountMoveInheritAdvance, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                                 submenu=submenu)
        if view_type == 'form' and self._context.get('default_custom_payment_type'):
            doc = etree.XML(res['arch'])
            domain = "[('type', '=', 'bank')]"
            for node in doc.xpath(f"//field[@name='journal_id']"):
                node.set('domain', domain)
                modifiers = json.loads(node.get("modifiers"))
                modifiers['domain'] = domain
                node.set("modifiers", json.dumps(modifiers))
            res['arch'] = etree.tostring(doc)
        return res

    @api.depends('journal_id')
    def _compute_payment_method_line_id(self):
        ''' Compute the 'payment_method_line_id' field.
        This field is not computed in '_compute_payment_method_fields' because it's a stored editable one.
        '''
        for pay in self:
            payment_type = pay.custom_payment_type
            available_payment_method_lines = pay.journal_id._get_available_payment_method_lines(payment_type)
            # Select the first available one by default.
            if pay.payment_method_line_id in available_payment_method_lines:
                pay.payment_method_line_id = pay.payment_method_line_id
            elif available_payment_method_lines:
                pay.payment_method_line_id = available_payment_method_lines[0]._origin
            else:
                pay.payment_method_line_id = False

    @api.depends('journal_id')
    def _compute_payment_method_line_fields(self):
        for pay in self:
            payment_type = pay.custom_payment_type
            pay.available_payment_method_line_ids = pay.journal_id._get_available_payment_method_lines(payment_type)

    def action_reconcile_lines(self):
        if sum(self.partial_lines.filtered(lambda x: x.reconciled_id).mapped('amount')) == self.adv_pay_amt and \
                self.partial_lines.filtered(lambda x: not x.reconciled_id):
            raise ValidationError('You cannot reconcile more Invoices\Bills.')
        if sum(self.partial_lines.filtered(lambda x: x.reconciled_id).mapped('amount')) == self.adv_pay_amt:
            raise ValidationError('You have reconciled all the line items')
        if self.partial_lines.filtered(lambda x: x.payment_line.id not in self.line_ids.ids):
            raise ValidationError('Incorrect Payment Selected For Reconciliation.')
        acc_type = 'receivable' if self.custom_payment_type == 'inbound' else 'payable'
        for rec in self.partial_lines.filtered(lambda x: not x.reconciled_id and x.amount > 0):
            payment_move_line = rec.payment_line
            if abs(payment_move_line.amount_residual) < rec.amount:
                raise ValidationError(f'You are only allowed to Reconcile {abs(payment_move_line.amount_residual)} '
                                      f'{payment_move_line.currency_id.symbol} for {rec.move_id.name}')
            data = {'amount': rec.amount,
                    'credit_amount_currency': rec.amount,
                    'debit_amount_currency': rec.amount,
                    'max_date': datetime.now().date()}
            move_line_id = rec.move_id.line_ids.filtered(lambda x: x.account_id.internal_type == acc_type)[0]
            data['debit_move_id'], data['credit_move_id'] = (move_line_id.id, payment_move_line.id) \
                if rec.move_id.move_type == 'out_invoice' else (payment_move_line.id, move_line_id.id)
            reconciled_id = self.env['account.partial.reconcile'].create(data)
            rec.reconciled_id = reconciled_id.id
            payment_move_line._compute_amount_residual()

    def validate_payment(self):
        if not self.partner_id:
            raise ValidationError("Partner is Mandatory")
        if sum(self.line_ids.mapped('debit')) != self.adv_pay_amt:
            raise ValidationError('Payment Amount and Sum of Line item should be same')
        if not self.line_ids.filtered(lambda x: x.account_id.id in self._get_valid_liquidity_accounts()):
            raise ValidationError('No Outstanding Account Found in Below Line Items')
        if not self.line_ids.filtered(lambda x: x.account_id.internal_type in ('payable', 'receivable')):
            raise ValidationError('Payable/Receivable Account Not Found')

    def action_post(self):
        res = super(AccountMoveInheritAdvance, self).action_post()
        if self._context.get('default_custom_payment_type'):
            self.validate_payment()
        return res

    @api.model
    def fields_get(self, fields=None, attributes=None):
        res = super(AccountMoveInheritAdvance, self).fields_get(fields, attributes)
        payment_type = self._context.get("default_custom_payment_type")
        if payment_type:
            if payment_type == 'inbound':
                domain = [('customer_rank', ">", 0)]
            elif payment_type == 'outbound':
                domain = [('supplier_rank', ">", 0)]
            res["partner_id"]["domain"] = domain
        return res

    @api.model
    def create(self, values):
        res = super(AccountMoveInheritAdvance, self).create(values)
        if self._context.get('advance_je'):
            res.validate_payment()
            if res.advance_ids.filtered(lambda x: x.advance_amount <= 0):
                raise ValidationError('Please Enter Advance Amount for below orders.')
            if res.adv_pay_amt != sum(res.advance_ids.mapped('advance_amount')):
                raise ValidationError('Sum of Advance Amount does not match the Payment Amount.')
        return res


class PaymentInherit(models.Model):
    _inherit = 'account.payment'

    partial_lines = fields.One2many('partial.line', 'payment_id')
    pending_amt = fields.Float(compute="compute_pending_amt")

    @api.depends('partial_lines.amount')
    def compute_pending_amt(self):
        amount = self.amount - sum(self.partial_lines.mapped('amount'))
        if amount < 0:
            raise ValidationError('You are trying to reconcile more than the payment amount')
        self.pending_amt = amount

    def action_reconcile_lines(self):
        acc_type = 'receivable' if self.payment_type == 'inbound' else 'payable'
        payment_move_line = self.move_id.line_ids.filtered(lambda x: x.account_id.internal_type == acc_type)[0]
        for rec in self.partial_lines.filtered(lambda x: not x.reconciled_id and x.amount > 0):
            data = {'amount': rec.amount,
                    'credit_amount_currency': rec.amount,
                    'debit_amount_currency': rec.amount,
                    'max_date': datetime.now().date()}
            move_line_id = rec.move_id.line_ids.filtered(lambda x: x.account_id.internal_type == acc_type)[0]
            data['debit_move_id'], data['credit_move_id'] = (move_line_id.id, payment_move_line.id) \
                if rec.move_id.move_type == 'out_invoice' else (payment_move_line.id, move_line_id.id)
            reconciled_id = self.env['account.partial.reconcile'].create(data)
            rec.reconciled_id = reconciled_id.id
        payment_move_line._compute_amount_residual()


class AccountMoveLineInherit(models.Model):
    _inherit = "account.move.line"

    is_os_line = fields.Boolean()


class PartialLines(models.Model):
    _name = 'partial.line'

    entry_id = fields.Many2one('account.move', auto_join=True)
    payment_line = fields.Many2one('account.move.line', string="Payment")
    move_id = fields.Many2one('account.move', required=True)
    payment_id = fields.Many2one('account.payment')
    partner_id = fields.Many2one('res.partner')
    move_amt = fields.Float(readonly=True, string="Move Amount")
    residual_amount = fields.Float(readonly=True, string="Residual Amount")
    amount = fields.Float()
    reconciled_id = fields.Many2one('account.partial.reconcile')

    @api.onchange('move_id')
    def set_required_data(self):
        for rec in self:
            rec.amount = 0
            if rec.move_id:
                rec.residual_amount = rec.move_id.amount_residual
                rec.move_amt = rec.move_id.amount_total_signed
            else:
                rec.residual_amount = rec.move_amt = 0

    @api.model
    def fields_get(self, fields=None, attributes=None):
        res = super(PartialLines, self).fields_get(fields, attributes)
        payment_type = self._context.get("default_custom_payment_type") or self._context.get('payment_type')
        if payment_type:
            if payment_type == 'inbound':
                domain = "[('move_type', '=', 'out_invoice'), ('state', '=', 'posted')," \
                         " ('partner_id', '=', partner_id), ('amount_residual', '>', 0)]"
                name, move_amt = "Invoices", 'Invoice Amount'
            else:
                domain = "[('move_type', '=', 'in_invoice'), ('state', '=', 'posted')," \
                         " ('partner_id', '=', partner_id), ('amount_residual', '>', 0)]"
                name, move_amt = "Bills", 'Bill Amount'
            res["move_id"]["domain"] = domain
            res["move_id"]["string"] = name
            res["move_amt"]["string"] = move_amt
        return res

    @api.onchange('amount')
    def validate_amount(self):
        if self.amount and self.amount > self.residual_amount:
            raise ValidationError(r'Amount should not be greater than Invoice\Bill Residual Amount.')

    @api.ondelete(at_uninstall=False)
    def verify_line_before_unlink(self):
        for rec in self:
            if rec.reconciled_id and rec.payment_id.state == 'posted':
                raise ValidationError('You cannot delete reconciled Lines')

    def button_undo_reconciliation(self):
        self.reconciled_id.unlink()

    @api.model
    def create(self, values):
        res = super(PartialLines, self).create(values)
        if res.entry_id:
            payment_type = 'receivable' if res.entry_id.custom_payment_type == 'inbound' else 'payable'
            payment_line = res.entry_id.line_ids.filtered(lambda x: x.account_id.internal_type == payment_type)
            if len(payment_line) == 1:
                res.payment_line = payment_line.id
        return res


class AdvanceOrder(models.Model):
    _name = 'advance.orders'

    sale_id = fields.Many2one('sale.order', domain=[('state', '=', 'sale')])
    purchase_id = fields.Many2one('purchase.order', domain=[('state', '=', 'purchase')])
    partner_id = fields.Many2one('res.partner')
    payment_terms = fields.Many2one('account.payment.term', readonly=True)
    order_amount = fields.Float(readonly=True)
    advance_amount = fields.Float()
    move_id = fields.Many2one('account.move', auto_join=True)

    @api.onchange('sale_id')
    def set_sales_field(self):
        self.payment_terms = self.sale_id.payment_term_id.id
        self.order_amount = self.sale_id.amount_total

    @api.onchange('purchase_id')
    def set_purchase_field(self):
        self.payment_terms = self.purchase_id.payment_term_id.id
        self.order_amount = self.purchase_id.amount_total

    @api.onchange('advance_amount')
    def validate_advance_amount(self):
        if self.advance_amount > self.order_amount:
            raise ValidationError('Advance Amount cannot be greater than the Order Amount.')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def view_advance_payment(self):
        je = self.env['advance.orders'].search([('sale_id', '=', self.id)])
        return {
            'name': "Advance Payment",
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', je.move_id.ids)],
            'context': {'create': False}
        }

    def create_advance_payment(self):
        if len(set(self.partner_id.ids)) > 1:
            raise ValidationError('You Can Create Advance Payment for one Customer at a time')
        if self.filtered(lambda x: x.state != 'sale'):
            raise ValidationError('You can only create advance payment for Order in Sale Stage.')
        advance_data = [(0, 0, {'sale_id': rec.id, 'partner_id': rec.partner_id.id,
                                'payment_terms': rec.payment_term_id.id, 'order_amount': rec.amount_total}) for rec in self]
        return {
            'name': "Advance Payment",
            'res_model': 'account.move',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'create': False, 'default_custom_payment_type': 'inbound', 'display_field': False,
                        'advance_je': True, 'default_partner_id': self[0].partner_id.id, 'default_is_advance': True,
                        'default_advance_ids': advance_data}
        }


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def view_advance_payment(self):
        je = self.env['advance.orders'].search([('purchase_id', '=', self.id)])
        return {
            'name': "Advance Payment",
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', je.move_id.ids)],
            'context': {'create': False}
        }

    def create_advance_payment(self):
        if len(set(self.partner_id.ids)) > 1:
            raise ValidationError('You Can Create Advance Payment for one Vendor at a time')
        if self.filtered(lambda x: x.state != 'purchase'):
            raise ValidationError('You can only create advance payment for order in Purchase Stage.')
        advance_data = [(0, 0, {'purchase_id': rec.id, 'partner_id': rec.partner_id.id, 'order_amount': rec.amount_total
                                , 'payment_terms': rec.payment_term_id.id}) for rec in self]
        return {
            'name': "Advance Payment",
            'res_model': 'account.move',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'create': False, 'default_custom_payment_type': 'outbound', 'display_field': False,
                        'advance_je': True, 'default_partner_id': self[0].partner_id.id, 'default_is_advance': True,
                        'default_advance_ids': advance_data}
        }
