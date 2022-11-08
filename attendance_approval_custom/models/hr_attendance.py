from odoo import models, fields , api , _


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    custom_state = fields.Selection([
        ('draft', 'New'),
        ('approve', 'Approved'),
        ('reject', 'Rejected')], 
        string='Status', 
        required=True, 
        readonly=True, 
        copy=False, 
        default='draft'
    )
    custom_approver_id = fields.Many2one(
        'res.users',
        string='Approved by', 
        readonly=True, 
        copy=False,
    )
    custom_reject_id = fields.Many2one(
        'res.users', 
        string='Rejected by', 
        readonly=True, 
        copy=False,
    )
    custom_reason_refuse = fields.Text(
        string='Reason for Reject',
        required=False,
        copy=False,
        readonly=True, 
    )
    
    def action_approve(self):
        self.write({
            'custom_state': 'approve',
            'custom_approver_id': self.env.uid
        })

    def action_reject(self):
        self.write({
            'custom_state': 'reject'
        })

    def action_draft(self):
        self.write({
            'custom_state': 'draft'
        })

