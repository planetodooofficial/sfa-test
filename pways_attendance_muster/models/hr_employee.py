from odoo import fields, api, models, _
from odoo.exceptions import ValidationError

class HrEmployee(models.Model):   
	_inherit = "hr.employee"

	join_date = fields.Date(string="Join Date",default=fields.Date.today())

class HrContract(models.Model):   
	_inherit = "hr.contract"

	work_hours = fields.Float(string="Work Hours", default=8)

class HrWorkEnteryTypr(models.Model):   
	_inherit = "hr.work.entry.type"

	is_paid = fields.Boolean(string="Is Paid")
