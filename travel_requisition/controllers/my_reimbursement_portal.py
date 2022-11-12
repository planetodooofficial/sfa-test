from odoo import http, _
from odoo.http import content_disposition, Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal
from datetime import date


class AllMyExpense(http.Controller):
    @http.route('/my/MyReimbursement/', website=True, auth='public')
    def display_my_expenses(self, sortby=None, **kw):
        searchbar_sortings = {
            'date': {'label': _('Expense Date'), 'order': 'date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        all_my_expenses = http.request.env['hr.expense'].search(
            [('state', '=', ('draft', 'reported', 'approved', 'done', 'refused')),
             ('payment_mode', '=', 'own_account')], order=order)
        return http.request.render('travel_requisition.portal_all_my_expenses_list', {
            'my_expenses': all_my_expenses,
            'page_name': 'pexpense',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })

    @http.route('/my/MyReimbursement/<model("hr.expense"):rexpense>', auth='public', website=True)
    def display_my_expense_detail(self, rexpense):
        return http.request.render('travel_requisition.my_expense_detail', {
            'rexpense': rexpense,
            'page_name': 'pexpense',
        })

    @http.route('/create/MyReimbursement', website=True, auth='public')
    def myreimbursement_form(self, **kw):
        # get current login user
        userid = request.env.user.employee_id
        demo = request.env['hr.expense'].sudo().search([('travel_requisition_opt', '=', False)])
        # demo = self._document_check_access('hr.expense')

        # get products based on search filter from many2one
        r_product = request.env['product.product'].sudo().search(
            [('travel_requisition', '=', False), ('can_be_expensed', '=', True)])

        # get current date
        cdate = date.today()

        # get default selected account based on search filter from many 2 one
        # account_id_def = request.env['account.account'].sudo().search(
        #     [('internal_type', '=', 'other'), ('code', '=', '210700')])
        # get all account list based on search filter from many 2 one
        # account_id = request.env['account.account'].sudo().search([('internal_type', '=', 'other')])

        # get currency from many 2 one
        # currency_name = request.env['res.currency'].sudo().search([])

        # get all account list based on search filter from many 2 many
        # tax_name = request.env['account.tax'].sudo().search(
        #     [('type_tax_use', '=', 'purchase'), ('price_include', '=', True)])

        # get all analytic account list based on search filter from many 2 one
        # analytic_account = request.env['account.analytic.account'].sudo().search([])

        # get all account list based on search filter from many 2 many
        # analytic_account_tag = request.env['account.analytic.tag'].sudo().search([])

        # get field for getting paid by value
        # paid_id = request.env['hr.expense']

        autofill_data = {
            # 'module_fields_name' : defined_fields_name
            'user': userid,
            'r_product': r_product,
            'cdate': cdate,
            'demo': demo,
            # 'currency_name': currency_name,
            # 'tax_name': tax_name,
            # 'analytic_account': analytic_account,
            # 'analytic_account_tag': analytic_account_tag,
            # 'account_id': account_id,
            # 'account_id_def': account_id_def,
            # 'paid_id': paid_id,
        }
        if kw:

            # writing if condition to get value from many 2 one if value not present then pass false to the field
            # if kw.get('tax_name'):
            #     # here tax_name many 2 many getting id in string is convert into integer and store in field
            #     tax_ids = int(kw.get('tax_name'))
            # else:
            #     # if tax_name not select then pass false
            #     tax_ids = False

            if kw.get('r_product'):
                # here r_product many 2 one getting id in string is convert into integer and store in field
                product_name = int(kw.get('r_product'))
            else:
                # if product not select then pass false
                product_name = False

            # if kw.get('account_id'):
            #     accountid = int(kw.get('account_id'))
            # else:
            #     accountid = False

            # if kw.get('analytic_account'):
            #     analytic_acc = int(kw.get('analytic_account'))
            # else:
            #     analytic_acc = False

            # if kw.get('analytic_account_tag'):
            #     # here analytic_account_tag many 2 many getting id in string is convert into integer and store in field
            #     analytic_tagid = int(kw.get('analytic_account_tag'))
            # else:
            #     # if analytic_account_tag not select then pass false
            #     analytic_tagid = False

            vals = {
                'name': kw.get('expname'),
                'product_id': product_name,
                'total_amount': kw.get('total_amount'),
                # this if condition and security condition is for many 2 many field
                # 'tax_ids': False if tax_ids is False else [(4, tax_ids)],

                # 'reference': kw.get('ref'),
                # 'account_id': accountid,
                # 'analytic_account_id': analytic_acc,

                # this if condition and security condition is for many 2 many field
                # 'analytic_tag_ids': False if analytic_tagid is False else [(4, analytic_tagid)],

                # don't know about this field, this field shows mandatory therefore i pass 1
                'unit_amount': 1,
                'payment_mode': 'own_account'
                # 'payment_mode': 'own_account' if kw.get('payment_mode') == 'own_account' else 'own_account'
            }

            # create method override to create record from form
            create_record = request.env['hr.expense'].sudo().create(vals)
        return http.request.render('travel_requisition.create_my_reimbursement', autofill_data)


class MyExpenseCustomerPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super(MyExpenseCustomerPortal, self)._prepare_home_portal_values(counters)
        count_my_expenses = request.env['hr.expense'].sudo().search_count(
            [('state', '=', ('draft', 'reported', 'approved', 'done', 'refused')),
             ('payment_mode', '=', 'own_account')])
        values.update({
            'count_my_expenses': count_my_expenses,
        })
        return values
