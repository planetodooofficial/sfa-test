from odoo import fields, models, api, _


class AnalyticAccountInherit(models.Model):
    _inherit = 'account.analytic.account'

    cost_profit_center = fields.Many2one('parent.head', string="Cost / Profit Centers")
    location = fields.Many2one('location.center', string="Location")
    departments = fields.Many2one('departments.center', string="Department")
    sub_departments = fields.Many2one('sub.departments', string="Sub Department")
    cost_profit_code = fields.Char(related='cost_profit_center.code')
    location_code = fields.Char(related='location.code')
    departments_code = fields.Char(related='departments.code')
    sub_departments_code = fields.Char(related='sub_departments.code')

    @api.onchange('cost_profit_center', 'location', 'departments', 'sub_departments')
    def set_analytic_account(self):
        self.name = f"{self.cost_profit_code or ''}{self.departments_code or ''}{self.sub_departments_code or ''}{self.location_code or ''}"

    def create_analytic_account(self):
        search_cost_profit = self.env['parent.head'].search([]).ids
        search_departments = self.env['departments.center'].search([]).ids
        search_sub_departments = self.env['sub.departments'].search([]).ids
        search_location = self.env['location.center'].search([]).ids

        # def create_analytic_account(self, cost_profit, departments, sub_departments, location):
        for i in search_cost_profit:
            for j in search_departments:
                for m in search_sub_departments:
                    for k in search_location:
                        code_cost_profit = self.env['parent.head'].search([('id', '=', i)]).mapped('code')
                        code_departments = self.env['departments.center'].search([('id', '=', j)]).mapped('code')
                        code_sub_departments = self.env['sub.departments'].search([('id', '=', m)]).mapped('code')
                        code_location = self.env['location.center'].search([('id', '=', k)]).mapped('code')
                        self.env['account.analytic.account'].create({
                            'name': f'{code_cost_profit[0]}{code_location[0]}{code_departments[0]}{code_sub_departments[0]}',
                            'cost_profit_center': i,
                            'departments': j,
                            'sub_departments': m,
                            'location': k,
                        })




        # create_analytic_account(self, search_cost_profit, search_departments, search_sub_departments, search_location)

