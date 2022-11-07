# -*- coding: utf-8 -*-
from odoo import fields, api, models, _
from odoo.exceptions import ValidationError
from datetime import timedelta
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import datetime
import pytz
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
import calendar

class HrAttendanceDashboard(models.Model):   
    _name = "hr.attendance.muster.dashboard"
    _description = "Employees Attendance Muster Dashboard"

    employee_ids = fields.Many2many('hr.employee', string="Resource")
    date_from = fields.Date(string='Date From', required=True, default=lambda self: fields.Date.to_string(date.today().replace(day=1)))
    date_to = fields.Date(string='Date To', required=True, default=lambda self: fields.Date.to_string((datetime.datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()))

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        if any(muster.date_from > muster.date_to for muster in self):
            raise ValidationError(_("Attendance Muster 'Date From' must be earlier 'Date To'."))

    def action_open_dashboard(self):
        active_id = self.env.context.get('active_id')
        return {
            'name': 'Dashboard',
            'type': 'ir.actions.client',
            'tag': 'attendance_dashboard',
            'context': "{'attendance_id': active_id}",
        }

    def _get_holiday_leave_data(self, employee_id, from_date, to_date, un_present_days):
        public_holiday_dates = []
        for date in un_present_days:
            date_start = date.strftime(DEFAULT_SERVER_DATE_FORMAT)
            holiday_ids = self.env['resource.calendar.leaves'].search([('date_from', '<=', date_start), ('date_to', '>=', date_start), ('resource_id', '=',False)])
            if holiday_ids:
                public_holiday_dates.append(date_start)
        return public_holiday_dates

    def dayNameFromWeekday(self, weekday):
        if weekday == 0:
            weeks = calendar.TextCalendar(calendar.MONDAY)
            return weeks
        if weekday == 1:
            weeks = calendar.TextCalendar(calendar.TUESDAY)
            return weeks
        if weekday == 2:
            weeks = calendar.TextCalendar(calendar.WEDNESDAY)
            return weeks
        if weekday == 3:
            weeks = calendar.TextCalendar(calendar.THURSDAY)
            return weeks
        if weekday == 4:
            weeks = calendar.TextCalendar(calendar.FRIDAY)
            return weeks
        if weekday == 5:
            weeks = calendar.TextCalendar(calendar.SATURDAY)
            return weeks
        if weekday == 6:
            weeks = calendar.TextCalendar(calendar.SUNDAY)
            return weeks

    def _get_weekoff_leave_data(self, employee_id):
        year = self.date_from.year
        month = self.date_from.month
        weekoff_dates = []
        total_days = [0,1,2,3,4,5,6]
        
        weekdays_id = employee_id.resource_calendar_id.attendance_ids.mapped('dayofweek')
        weekoffdays_set = set(weekdays_id)
        total_weekday = list(weekoffdays_set)
        res = [eval(i) for i in total_weekday]
        weekoff = [x for x in total_days if x not in res]

        for week in weekoff:
            weeks = self.dayNameFromWeekday(week)
            for wekday in weeks.itermonthdays(year,month):
                if wekday != 0:
                    day = date(year,month,wekday)
                    if day.weekday() == week:
                        first_day = (str(year) + "-" + str(month) + "-" + str(wekday))
                        first_date = datetime.datetime.strptime(first_day, '%Y-%m-%d').date()
                        weekoff_dates.append(first_date.strftime('%Y-%m-%d'))
        return weekoff_dates

    def _get_paid_leave_data(self, employee_id, un_present_days):
        leave_ids = self.env['hr.leave']
        paid_leave_days = 0.0
        paid_dates = []
        for date in un_present_days:
            leave_domain = [
                ('state', '=', 'validate'),
                ('employee_id', '=', employee_id.id),
                ('request_date_from', '<=', date),
                ('request_date_to', '>=', date),
                ('holiday_status_id.work_entry_type_id.is_paid', '=', True)]
            paid_leave_ids = self.env['hr.leave'].search(leave_domain)
            leave_ids |= paid_leave_ids

        for paid in leave_ids:
            delta = paid.request_date_to - paid.request_date_from
            paid_days = paid.request_date_from
            for i in range(delta.days + 1):
                days = paid_days + timedelta(days=i)
                paid_dates.append(days.strftime(DEFAULT_SERVER_DATE_FORMAT))

        paid_leave_days = sum(leave_ids.mapped('number_of_days'))
        return paid_dates, paid_leave_days

    def _get_unpaid_leave_data(self, employee_id, un_present_days):
        leave_ids = self.env['hr.leave']
        unpaid_leave_days = 0.0
        unpaid_dates = []
        for date in un_present_days:
            leave_domain = [
                ('state', '=', 'validate'),
                ('employee_id', '=', employee_id.id),
                ('holiday_status_id.work_entry_type_id.is_paid', '=', False),
                ('request_date_from', '<=', date),
                ('request_date_to', '>=', date)]
            unpaid_leave_ids = self.env['hr.leave'].search(leave_domain)
            leave_ids |= unpaid_leave_ids

        for unpaid in leave_ids:
            delta = unpaid.request_date_to - unpaid.request_date_from
            unpaid_days = unpaid.request_date_from
            for i in range(delta.days + 1):
                days = unpaid_days + timedelta(days=i)
                unpaid_dates.append(days.strftime(DEFAULT_SERVER_DATE_FORMAT))

        unpaid_leave_days = sum(leave_ids.mapped('number_of_days'))
        return unpaid_dates, unpaid_leave_days

    def get_employees_attendance_muster_data(self, attendance_id=None):
        from_date = self.date_from
        to_date = self.date_to
        employee_ids = self.employee_ids
        employee_data = {}
        emp_list = []
        header_date = []
        header_list = []

        if from_date and to_date:
            delta_date = to_date - from_date
            all_days = [from_date + timedelta(days=i) for i in range(delta_date.days + 1)]

            header_date.append({
                'start_date' : from_date.strftime("%d-%m-%Y"),
                'end_date': to_date.strftime("%d-%m-%Y"),
                })

            for spec_date in all_days:
                header_list.append(spec_date.strftime("%d"))
            header_list.extend(['P', 'A', 'UL', 'PL', 'WO', 'H', 'A/H', 'Paid Days'])
            domain = [('check_in', '>=', from_date), ('check_out', '<=', to_date)]

            if employee_ids:
                    domain.append(('employee_id', 'in', employee_ids.ids))
            attendance_ids = self.env['hr.attendance'].search(domain)
            for rec in attendance_ids:
                if rec.employee_id.id not in employee_data:
                    employee_data[rec.employee_id.id] = rec
                else:
                    employee_data[rec.employee_id.id] |= rec

            # emp wise data
            for key, values in employee_data.items():
                employee_id = self.env['hr.employee'].browse(key)
                fil_date = []
                worked_hours_list = []
                total_list = []
                att_hours = 0.0
                day_list = []
                # other data
                if employee_id:
                    state = 'N/A'
                    original_hire_date = str(employee_id.join_date)
                    company_id = self.env.company
                    contract_id = employee_id.contract_ids.filtered(lambda x: x.state == 'open')
                    if contract_id:
                        state = dict(contract_id._fields['state'].selection).get(contract_id.state)
                        working_hours = contract_id.work_hours
                    emp_list.append({
                        'id': employee_id.id,
                        'employee_id': employee_id.name,
                        'position': employee_id.job_id.name,
                        'hire_date': original_hire_date if original_hire_date else False,
                        'std_work_hrs': company_id.work_hours or working_hours,
                        'contract_status': state,
                        'worked_hours_list': worked_hours_list,
                        'total_records': total_list,
                    })

                    # get all dates
                    for date in values.mapped('check_in'):
                        fil_date.append(date.date())
                    #add calulative methods
                    for f_date in fil_date:
                        day_list.append(fields.Date.to_string(f_date))

                    un_present_days = set(all_days) - set(fil_date)
                    unpaid_dates, unpaid_leave_days = self._get_unpaid_leave_data(employee_id, un_present_days)
                    paid_dates, paid_leave_days = self._get_paid_leave_data(employee_id, un_present_days)
                    weekoff_dates = self._get_weekoff_leave_data(employee_id)
                    public_holiday_dates = self._get_holiday_leave_data(employee_id, from_date, to_date, un_present_days)
                    
                    to_filter_week_off = list(set(public_holiday_dates + paid_dates + unpaid_dates))
                    to_filter_holidays = list(set(paid_dates + unpaid_dates))

                    fil_weekoff_dates = list(set(weekoff_dates) - set(to_filter_week_off))
                    fil_holiday_dates = list(set(public_holiday_dates) - set(to_filter_holidays))

                    holiday_dates = fil_weekoff_dates + paid_dates + unpaid_dates + fil_holiday_dates

                    total_p_days = set(day_list) - set(holiday_dates)
                    present_day = len(total_p_days)
                    public_holidays_days = len(fil_holiday_dates)
                    week_off_days = len(fil_weekoff_dates)
                    total_days = week_off_days + unpaid_leave_days + paid_leave_days + public_holidays_days + present_day

                    #absent days
                    total_absent_days = 0
                    absent_days = len(all_days) - total_days
                    if absent_days >= 0:
                        total_absent_days = absent_days

                    att_hours = round(sum(values.mapped('worked_hours')),2)
                    total_records = paid_leave_days + present_day + week_off_days + public_holidays_days
                    total_list.append({
                        'present': present_day if present_day else 0,
                        'absent': total_absent_days if total_absent_days else 0,
                        'week_off_records': week_off_days if week_off_days else 0,
                        'unpaid_leave_records': unpaid_leave_days if unpaid_leave_days else 0,
                        'paid_leave_records': paid_leave_days if paid_leave_days else 0,
                        'holidays_records': public_holidays_days if public_holidays_days else 0,
                        'attendance_hours_records': att_hours,
                        'total_records': total_records,
                        })

                    # get all dates
                    for spec_date in all_days:
                        worked_hours = ""

                        if spec_date in fil_date:
                            att_rec = values.filtered(lambda x: x.check_in.date() == spec_date)
                            worked_hours = round(sum(att_rec.mapped('worked_hours')),2)

                        else:
                            if str(spec_date) in paid_dates:
                                worked_hours = "PL"

                            elif str(spec_date) in unpaid_dates:
                                worked_hours = "UL"

                            elif str(spec_date) in fil_holiday_dates:
                                worked_hours += "H"

                            elif str(spec_date) in fil_weekoff_dates:
                                worked_hours += "WO"

                            else:
                                worked_hours = "A"
                        worked_hours_list.append(worked_hours)           
            return {
                'employee_ids': emp_list,
                'header_date': header_date,
                'header_list': header_list,
                }
