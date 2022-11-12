# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    work_hours = fields.Float(related="company_id.work_hours", string="Work Hours", readonly=False)


class ResCompany(models.Model):
    _inherit = 'res.company'

    work_hours = fields.Float(string="Work Hours", default=8)
