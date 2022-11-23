from odoo import http, _
from odoo.http import content_disposition, Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal
from datetime import date, datetime, time, timedelta


class AllExpense(http.Controller):
    @http.route('/my/TravelRequisition/', website=True, auth='public')
    def display_expenses(self, sortby=None, **kw):
        searchbar_sortings = {
            'date': {'label': _('Expense Date'), 'order': 'date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        all_expenses = http.request.env['hr.expense'].search(
            [('state', '=', ('draft', 'reported', 'approved', 'done', 'refused')),
             ('payment_mode', '=', 'company_account')], order=order)
        return http.request.render('travel_requisition.portal_all_expenses_list', {
            'expenses': all_expenses,
            'page_name': 'expense',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })

    @http.route('/my/TravelRequisition/<model("hr.expense"):expense>', auth='public', website=True)
    def display_expense_detail(self, expense, **kw):
        # this part for add line of one to many field
        t_mode_class = request.env['mode.class.master'].sudo().search([])

        # field to get current login user id
        userid = request.env.user.employee_id
        # field for auto field data
        user_info = request.env['hr.employee'].sudo().browse(userid.id)

        if kw.get('travel_detail_line_create'):
            # all fields related to Travel details one to many
            if kw.get('t_mode_class'):
                t_modeclass = int(kw.get('t_mode_class'))
            else:
                t_modeclass = False

            if kw.get('t_date'):
                rdate = kw.get('t_date')
            else:
                rdate = False

            if kw.get('t_from'):
                rfrom = kw.get('t_from')
            else:
                rfrom = False

            if kw.get('t_mode_class'):
                rdepartstime = float(kw.get('t_depart_time').replace(":", "."))
            else:
                rdepartstime = False

            if kw.get('t_to'):
                rto = kw.get('t_to')
            else:
                rto = False

            if kw.get('t_arrive_time'):
                rarrivetime = float(kw.get('t_arrive_time').replace(":", "."))
            else:
                rarrivetime = False

            lines = {
                'hr_exp_id': expense.id,
                'date': datetime.strptime(rdate,'%Y-%m-%d').date(),
                'from_dates': datetime.strptime(rfrom, '%Y-%m-%d').date(),
                'to_dates': datetime.strptime(rto, '%Y-%m-%d').date(),
                'departs_time': rdepartstime,
                'arrives_time': rarrivetime,
                'mode_and_class': t_modeclass,
            }
            traveldata = request.env['travel.details.line'].sudo().create(lines)
            if traveldata:
                return request.redirect('/my/TravelRequisition/%s' % expense.id)

        if kw.get('stay_detail_line_create'):
            # all fields related to stay details one to many
            rstayname = kw.get('t_stay_name')
            rhotelguest = kw.get('t_hotelguest')
            rlocation = kw.get('t_location')
            if kw.get('t_checkin_date'):
                rcheckindate = kw.get('t_checkin_date')
            else:
                rcheckindate = False
            if kw.get('t_checkout_date'):
                rcheckoutdate = kw.get('t_checkout_date')
            else:
                rcheckoutdate = False

            stay_lines = {
                'hr_exp_id': expense.id,
                'hotel_guest_line': rhotelguest,
                'location_line': rlocation,
                'check_in_date': datetime.strptime(rcheckindate, '%Y-%m-%d').date(),
                'check_out_date': datetime.strptime(rcheckoutdate, '%Y-%m-%d').date(),
            }
            staydata = request.env['stay.details.line'].sudo().create(stay_lines)

            if staydata:
                return request.redirect('/my/TravelRequisition/%s' % expense.id)

        return http.request.render('travel_requisition.expense_detail', {
            'expense': expense,
            'page_name': 'expense',
            't_mode_class': t_mode_class,
            't_stay_name': user_info,
        })

    @http.route('/create/TravelRequisition', website=True, auth='public')
    def travelrequisition_form(self, **kw):
        # get current login user
        userid = request.env.user.employee_id

        # get products based on search filter from many 2 one
        t_product = request.env['product.product'].sudo().search(
            [('travel_requisition', '=', True), ('can_be_expensed', '=', True)])

        # get current date
        cdate = date.today()

        # for getting travel requisition field values
        t_purpose = request.env['hr.expense'].sudo().search([])

        t_mode_class = request.env['mode.class.master'].sudo().search([])
        user_info = request.env['hr.employee'].sudo().browse(userid.id)

        autofill_data = {
            # 'key' : mention fields
            'user': userid,
            't_product': t_product,
            'cdate': cdate,

            't_empcode': user_info,
            't_comp': user_info,
            't_mob': user_info,
            't_department': user_info,
            't_gr': user_info,
            't_desig': user_info,
            't_cad': user_info,
            't_grat': user_info,

            't_mode_class': t_mode_class,

            't_pan_card': user_info,
            't_driving_li': user_info,
            't_age': user_info,
            't_passport_name': user_info,
            't_pass_no': user_info,
            't_place_issue': user_info,
            't_date_issue': user_info,

            't_stay_name': user_info,
        }
        if kw:

            # writing if condition to get value from many 2 one if value not present then pass false to the field
            if kw.get('t_product'):
                # here r_product many 2 one getting id in string is convert into integer and store in field
                product_name = int(kw.get('t_product'))
            else:
                # if product not select then pass false
                product_name = False

            # all fields related to travel detail one to many
            if kw.get('t_mode_class'):
                # here t_mode_class many 2 one getting id in string is convert into integer and store in field
                t_modeclass = int(kw.get('t_mode_class'))
            else:
                t_modeclass = False

            if kw.get('t_date'):
                rdate = kw.get('t_date')

            if kw.get('t_from'):
                rfrom = kw.get('t_from')

            if kw.get('t_depart_time'):
                # rdepartstime = float(kw.get('t_depart_time'))
                rdepartstime = float(kw.get('t_depart_time').replace(":", "."))
            else:
                rdepartstime = False

            if kw.get('t_to'):
                rto = kw.get('t_to')

            if kw.get('t_arrive_time'):
                rarrivetime = float(kw.get('t_arrive_time').replace(":", "."))
            else:
                rarrivetime = False

            # all fields related to stay details one to many
            if kw.get('t_stay_name'):
                rstayname = kw.get('t_stay_name')

            if kw.get('t_hotelguest'):
                rhotelguest = kw.get('t_hotelguest')

            if kw.get('t_location'):
                rlocation = kw.get('t_location')

            if kw.get('t_checkin_date'):
                rcheckindate = kw.get('t_checkin_date')

            if kw.get('t_checkout_date'):
                rcheckoutdate = kw.get('t_checkout_date')

            tvals = {
                'name': kw.get('t_expname'),
                'product_id': product_name,
                'total_amount': kw.get('t_total_amount'),
                # don't know about this field, this field shows mandatory therefore i pass 1
                'unit_amount': 1,
                'payment_mode': 'company_account',
                'purpose_of_visit': kw.get('t_purpose'),
            }

            # create method override to create record from form
            create_record = request.env['hr.expense'].sudo().create(tvals)

            lines = {
                'hr_exp_id': int(create_record.id),
                'date': datetime.strptime(rdate, '%Y-%m-%d').date(),
                'from_dates': datetime.strptime(rfrom, '%Y-%m-%d').date(),
                'to_dates': datetime.strptime(rto, '%Y-%m-%d').date(),
                'departs_time': rdepartstime,
                'arrives_time': rarrivetime,
                'mode_and_class': t_modeclass,
            }
            traveldata = request.env['travel.details.line'].sudo().create(lines)

            stay_lines = {
                'hr_exp_id': create_record.id,
                'hotel_guest_line': rhotelguest,
                'location_line': rlocation,
                'check_in_date': datetime.strptime(rcheckindate, '%Y-%m-%d').date(),
                'check_out_date': datetime.strptime(rcheckoutdate, '%Y-%m-%d').date(),
            }
            staydata = request.env['stay.details.line'].sudo().create(stay_lines)

            # create_record.sudo().update(
            # {
            #     'travel_detail_line_ids': [(4, traveldata.id)],
            #     'stay_detail_line_ids': [(4, staydata.id)],
            # })

            # it can redirect to the created record after submit
            if create_record:
                return request.redirect('/my/TravelRequisition/%s' % create_record.id)

        return http.request.render('travel_requisition.create_travel_requisition', autofill_data)


class ExpenseCustomerPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super(ExpenseCustomerPortal, self)._prepare_home_portal_values(counters)
        count_expenses = http.request.env['hr.expense'].search_count(
            [('state', '=', ('draft', 'reported', 'approved', 'done', 'refused')),
             ('payment_mode', '=', 'company_account')])
        values.update({
            'count_expenses': count_expenses,
        })
        return values
