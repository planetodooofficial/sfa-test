from odoo import models, fields, api, _


class TravelRequisitionExpense(models.Model):
    _inherit = 'hr.expense'

    name_new = fields.Many2one('hr.employee', string='Name')
    emp_code = fields.Char(string='Employee Code', related='name_new.emp_code', store=True)
    band = fields.Char(string='Band')
    mobile = fields.Char(string='Mobile No.', related='name_new.mobile_phone', store=True)
    designation = fields.Char(string='Designation', related='name_new.job_title', store=True)
    department = fields.Char(string='Department', related='name_new.department_id.name', store=True)
    company = fields.Char(string='Company', related='name_new.company_id.name', store=True)
    purpose_of_visit = fields.Char(string='Purpose of Visit')
    approved_by = fields.Char(string='Approved By', related='name_new.parent_id.name', store=True)
    pan_dl_no = fields.Char(string='Pan Card Number', related='name_new.pan_no', store=True)
    dl_number = fields.Char(string='Driving License Number', related='name_new.dl_no', store=True)
    age = fields.Integer(string='Age')
    pass_name = fields.Char(string='Name on Passport', related='name_new.name_on_passport', store=True)
    pass_no = fields.Char(string='Passport No.', related='name_new.passport_id', store=True)
    date_place = fields.Char(string='Date & Place of Issue')
    visa_required = fields.Boolean(string='Visa Required')
    travel_detail_line_ids = fields.One2many('travel.details.line', 'hr_exp_id', 'Travel Detail Line')
    stay_detail_line_ids = fields.One2many('stay.details.line', 'hr_exp_id', 'Stay Detail Line')
    travel_requisition_opt = fields.Boolean(string='Travel Requisition')

    # function for product fields = when travel requisition product is selected then function set paid by field on Company
    # @api.onchange('product_id')
    # def _onchange_product_expense(self):
    #     if self.product_id:
    #         if self.product_id.travel_requisition == True:
    #             self.payment_mode = 'company_account'

class TravelDetailsLine(models.Model):
    _name = 'travel.details.line'

    hr_exp_id = fields.Many2one('hr.expense', string='Hr Expense Id')
    date = fields.Date(string='Date')
    from_dates = fields.Date(string='From')
    to_dates = fields.Date(string='To')
    departs_time = fields.Float(string='Departs Time')
    arrives_time = fields.Float(string='Arrives Time')
    mode_and_class = fields.Char(string='Mode & Class')


class StayDetailsLine(models.Model):
    _name = 'stay.details.line'

    hr_exp_id = fields.Many2one('hr.expense', string='Hr Expense Id')
    name_line = fields.Many2one('hr.employee', string='Name')
    band_line = fields.Char(string='Band')
    hotel_guest_line = fields.Char(string='Hotel / Guest House')
    location_line = fields.Char(string='Location')
    check_in_date = fields.Date(string='Check in Date')
    check_out_date = fields.Date(string='Check Out Date')


class ExpenseProductInherit(models.Model):
    _inherit = 'product.product'

    travel_requisition = fields.Boolean('Travel Requisitions')


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    emp_code = fields.Char(string='Employee Code')
    name_on_passport = fields.Char(string='Name on Passport')
    dl_no = fields.Char(string="Driving License Number")
    pan_no = fields.Char(string='Pan Card Number')
