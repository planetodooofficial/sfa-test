from odoo import http, _
from odoo.http import content_disposition, Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal
from datetime import date
import base64
from werkzeug.utils import redirect
import io


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

    @http.route(['/my/MyReimbursement/<model("hr.expense"):rexpense>'], type='http', auth='public', website=True)
    def display_my_expense_detail(self, rexpense):

        # field for show attached file in record on website form
        attachments = request.env['ir.attachment'].search(
            [('res_model', '=', 'hr.expense'),
             ('res_id', '=', rexpense.id)], order='id')

        return http.request.render('travel_requisition.my_expense_detail', {
            'rexpense': rexpense,
            'page_name': 'pexpense',
            'attachments': attachments,
        })

    # this function for show attachment on webform which is already attached
    @http.route(['/attachment/download', ], type='http', auth='public')
    def download_attachment(self, attachment_id):
        # Check if this is a valid attachment id
        attachment = request.env['ir.attachment'].search([('id', '=', int(attachment_id))])

        if attachment:
            attachment = attachment[0]
        else:
            return redirect('/my/MyReimbursement/')

        if attachment["type"] == "url":
            if attachment["url"]:
                return redirect(attachment["url"])
            else:
                return request.not_found()
        elif attachment["datas"]:
            data = io.BytesIO(base64.standard_b64decode(attachment["datas"]))
            return http.send_file(data, filename=attachment['name'], as_attachment=True)
        else:
            return request.not_found()

    @http.route('/create/MyReimbursement', website=True, auth='public')
    def myreimbursement_form(self, **kw):
        # get current login user
        userid = request.env.user.employee_id
        demo = request.env['hr.expense'].search([('travel_requisition_opt', '=', False)])

        # get products based on search filter from many2one
        r_product = request.env['product.product'].search(
            [('travel_requisition', '=', False), ('can_be_expensed', '=', True)])

        # get current date
        cdate = date.today()

        # sequence add from portal
        # seq_id = request.env['ir.sequence'].search([('code', '=', 'my.reimburse.code')])
        # seq_pool = request.env['ir.sequence']
        # app_no = seq_pool.get_id(seq_id.id)

        # field for attachment add
        files = request.httprequest.files.getlist('myfile')
        print(files, "this is file")
        attachment_id = []

        autofill_data = {
            # 'module_fields_name' : defined_fields_name
            'user': userid,
            'r_product': r_product,
            'cdate': cdate,
            'demo': demo,
        }

        if kw:
            if kw.get('r_product'):
                # here r_product many 2 one getting id in string is convert into integer and store in field
                product_name = int(kw.get('r_product'))
            else:
                # if product not select then pass false
                product_name = False

            vals = {
                # 'hr_sequence': app_no,
                'name': kw.get('expname'),
                'product_id': product_name,
                'total_amount': kw.get('total_amount'),
                # don't know about this field, this field shows mandatory therefore i pass 1
                'unit_amount': 1,
                'payment_mode': 'own_account'
            }

            # create method override to create record from form
            create_record = request.env['hr.expense'].create(vals)

            # this code related to add attachment from website
            if kw.get('myfile', False):
                Attachments = request.env['ir.attachment']
                files = request.httprequest.files.getlist('myfile')
                # file = kwargs.get('myfile', False)
                for file in files:
                    attachment = file.read()
                    attachment_id = Attachments.create({
                        'name': file.filename,
                        'display_name': 'new',
                        'res_name': 'new',
                        'type': 'binary',
                        'res_model': 'hr.expense',
                        'res_id': create_record.id,
                        'datas': base64.standard_b64encode(attachment)
                    })
                    print(attachment_id)

                showdata = create_record.update(
                    {'expense_document': attachment_id.datas, 'expensename': attachment_id.display_name})

                # it can redirect to the created record after submit
                if create_record:
                    return request.redirect('/my/MyReimbursement/%s' % create_record.id)

        return http.request.render('travel_requisition.create_my_reimbursement', autofill_data)


class MyExpenseCustomerPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super(MyExpenseCustomerPortal, self)._prepare_home_portal_values(counters)
        count_my_expenses = request.env['hr.expense'].search_count(
            [('state', '=', ('draft', 'reported', 'approved', 'done', 'refused')),
             ('payment_mode', '=', 'own_account')])
        values.update({
            'count_my_expenses': count_my_expenses,
        })
        return values
