from odoo import fields, api, models, _
from itertools import combinations


class AnalyticAccountWizards(models.TransientModel):
    _name = 'analytic.wizards'

    name = fields.Char(string="Name")

    def create_analytic_accounts(self):
        search_cost_profit = self.env['parent.head'].search([]).ids
        search_departments = self.env['departments.center'].search([]).ids
        search_sub_departments = self.env['sub.departments'].search([]).ids
        search_location = self.env['location.center'].search([]).ids

        def create_analytic_account(search_cost_profit, search_departments, search_sub_departments, search_location):
            for i in search_cost_profit:
                for j in search_departments:
                    for m in search_sub_departments:
                        for k in search_location:
                            code_cost_profit = self.env['parent.head'].search([('id', '=', i)]).mapped('code')
                            code_departments = self.env['departments.center'].search([('id', '=', j)]).mapped('code')
                            code_sub_departments = self.env['sub.departments'].search([('id', '=', m)]).mapped('code')
                            code_location = self.env['location.center'].search([('id', '=', k)]).mapped('code')
                            self.env['account.analytic.account'].create({
                                'name': f'{code_cost_profit[0]}{code_departments[0]}{code_sub_departments[0]}{code_location[0]}',
                                'cost_profit_center': i,
                                'departments': j,
                                'sub_departments': m,
                                'location': k,
                            })

        create_analytic_account(search_cost_profit, search_departments, search_sub_departments, search_location)








