from lxml import etree

from odoo import models, fields, api, _


class TravelRequisitionExpense(models.Model):
    _inherit = 'hr.expense'

    # sequence for my reimbursement & travel requisition
    hr_sequence = fields.Char(string='No.', required=True, copy=False, readonly=True, index=True,
                              default=lambda self: _('New'))

    # name_new = fields.Many2one('hr.employee', string='Name', default=(lambda self: self.env.user))
    emp_code = fields.Char(string='Employee Code', related='employee_id.emp_code', store=True)
    mobile = fields.Char(string='Mobile No.', related='employee_id.mobile_phone', store=True)
    designation = fields.Char(string='Designation', related='employee_id.job_title', store=True)
    department = fields.Char(string='Department', related='employee_id.department_id.name', store=True)
    company = fields.Char(string='Company', related='employee_id.company_id.name', store=True)
    purpose_of_visit = fields.Text(string='Purpose of Visit')
    pan_no_new = fields.Char(string='Pan Card Number', related='employee_id.pan', store=True)
    dl_number = fields.Char(string='Driving License Number', related='employee_id.dl_no', store=True)
    age = fields.Char(string='Age', related='employee_id.age', store=True)
    pass_name = fields.Char(string='Name on Passport', related='employee_id.name_on_passport', store=True)
    pass_no = fields.Char(string='Passport No.', related='employee_id.passport_id', store=True)
    pass_issue_date = fields.Date(string='Passport Issue Date', related='employee_id.emp_pass_issue_date', store=True)
    pass_issue_loc = fields.Char(string='Passport Issue location', related='employee_id.emp_pass_issue_loc', store=True)
    visa_required = fields.Boolean(string='Visa Required')

    t_grade = fields.Many2one('grade.master', string='Grade', related='employee_id.grade')
    t_cadre = fields.Many2one('cadre.master', string='Cadre', related='employee_id.cadre')
    t_grade_title = fields.Many2one('grade.title.master', string='Grade Title', related='employee_id.grade_title')

    travel_detail_line_ids = fields.One2many('travel.details.line', 'hr_exp_id', 'Travel Detail Line', required=True)
    stay_detail_line_ids = fields.One2many('stay.details.line', 'hr_exp_id', 'Stay Detail Line', required=True)
    travel_requisition_opt = fields.Boolean(string='Travel Requisition', default=False)

    expense_document = fields.Binary('Add Attachment')
    expensename = fields.Char('File Name')

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     res = super(TravelRequisitionExpense, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
    #                                                           submenu=submenu)
    #     if view_type == 'form':
    #         expense = [("travel_requisition", "=", True)] if self._context.get('travel_requisition_opt') is True else [
    #             ("travel_requisition", "=", False)]
    #         doc = etree.XML(res['arch'])
    #         for node in doc.xpath(f"//field[@name='product_id']"):
    #             node.set('domain', f"{expense}")
    #             res['arch'] = etree.tostring(doc)
    #     return res

    # product id field for travel requisition to filter product list based on menu selected
    # travel_product_id = fields.Many2one('product.product', string='Product', readonly=False, tracking=True,
    #                                     states={'draft': [('readonly', False)], 'reported': [('readonly', False)],
    #                                             'approved': [('readonly', False)], 'refused': [('readonly', False)]},
    #                                     domain="[('can_be_expensed', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id), ('travel_requisition','=',True)]",
    #                                     ondelete='restrict')

    # product_id actual field override and pass the context for the field
    product_id = fields.Many2one('product.product', string='Product', readonly=False, tracking=True,
                                 states={'draft': [('readonly', False)], 'reported': [('readonly', False)],
                                         'approved': [('readonly', False)], 'refused': [('readonly', False)]},
                                 domain="[('can_be_expensed', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id), ('travel_requisition', '=', context.get('travel_prd', False))]",
                                 ondelete='restrict')

    # function for product fields = when travel requisition product is selected then function set paid by field on Company
    # @api.onchange('product_id')
    # def _onchange_product_expense(self):
    #     if self.product_id:
    #         if self.product_id.travel_requisition == True:
    #             self.payment_mode = 'company_account'

    # CREATING DOMAIN ON PRODUCT_ID FIELD TO DIFFERENTIATE DATA BASED ON FIELD TRUE AND FALSE
    # @api.depends('travel_requisition_opt')
    # def _ondepends_product_id_view(self):
    #     domain = {}
    #     if self.travel_requisition_opt:
    #         if self.travel_requisition_opt == True & self.payment_mode == 'company_account':
    #             domain = {'product_id': [('product_id.travel_requisition', '=', True)]}
    #         if self.travel_requisition_opt == False & self.payment_mode == 'own_account':
    #             domain = {'product_id': [('product_id.travel_requisition', '=', False)]}
    #         return {'domain': domain}

    # sequence is differenciate for my reimbursement and travel requisition
    @api.model
    def create(self, vals):
        if vals.get('hr_sequence', _('New')) == _('New'):
            if self.env.context.get('default_travel_requisition_opt'):
                vals['hr_sequence'] = self.env['ir.sequence'].next_by_code('travel.requisition.code') or _('New')
            else:
                vals['hr_sequence'] = self.env['ir.sequence'].next_by_code('my.reimburse.code') or _('New')
        return super(TravelRequisitionExpense, self).create(vals)

    class TravelDetailsLine(models.Model):
        _name = 'travel.details.line'

        hr_exp_id = fields.Many2one('hr.expense', string='Hr Expense Id')
        date = fields.Date(string='Date')
        from_dates = fields.Date(string='From date')
        to_dates = fields.Date(string='To Date')
        departs_time = fields.Float(string='Departs Time')
        arrives_time = fields.Float(string='Arrives Time')
        mode_and_class = fields.Many2one('mode.class.master', string='Mode & Class')

    class StayDetailsLine(models.Model):
        _name = 'stay.details.line'

        hr_exp_id = fields.Many2one('hr.expense', string='Hr Expense Id')
        name_line = fields.Many2one('hr.employee', string='Name', related='hr_exp_id.employee_id')
        hotel_guest_line = fields.Char(string='Hotel / Guest House')
        location_line = fields.Char(string='Location')
        check_in_date = fields.Date(string='Check in Date')
        check_out_date = fields.Date(string='Check Out Date')

    class ExpenseProductInherit(models.Model):
        _inherit = 'product.product'

        travel_requisition = fields.Boolean('Travel Requisitions')
