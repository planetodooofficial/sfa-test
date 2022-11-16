# from odoo import fields, models, api, _
#
#
# class AdvancePaymentWizard(models.TransientModel):
#     _name = 'advance.payment.wizard'
#
#     journal_id = fields.Many2one('account.journal', string='Journal', required=True, domain="[('type', '=', 'bank')]")
#     payment_method_line_id = fields.Many2one('account.payment.method.line', string='Payment Method',
#                                              readonly=False, store=True, copy=False,
#                                              compute='_compute_payment_method_line_id',
#                                              domain="[('id', 'in', available_payment_method_line_ids)]")
#     available_payment_method_line_ids = fields.Many2many('account.payment.method.line',
#                                                          compute='_compute_payment_method_line_fields')
#     custom_payment_type = fields.Selection([('inbound', 'Inbound'), ('outbound', 'Outbound')])
#     amount = fields.Float()
#
#     @api.depends('journal_id')
#     def _compute_payment_method_line_id(self):
#         ''' Compute the 'payment_method_line_id' field.
#         This field is not computed in '_compute_payment_method_fields' because it's a stored editable one.
#         '''
#         for pay in self:
#             payment_type = pay.custom_payment_type
#             available_payment_method_lines = pay.journal_id._get_available_payment_method_lines(payment_type)
#             # Select the first available one by default.
#             if pay.payment_method_line_id in available_payment_method_lines:
#                 pay.payment_method_line_id = pay.payment_method_line_id
#             elif available_payment_method_lines:
#                 pay.payment_method_line_id = available_payment_method_lines[0]._origin
#             else:
#                 pay.payment_method_line_id = False
#
#     @api.depends('journal_id')
#     def _compute_payment_method_line_fields(self):
#         for pay in self:
#             payment_type = pay.custom_payment_type
#             pay.available_payment_method_line_ids = pay.journal_id._get_available_payment_method_lines(payment_type)
#
#
# class AdvancePaymentLineWizard(models.TransientModel):
#     _name = 'advance.'
