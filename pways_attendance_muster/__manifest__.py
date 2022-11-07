# -*- coding: utf-8 -*-
{
    'name': 'Employee Attendances Muster',
    'summary': 'Employee attendances muster which shows all require data including (daily attendances, present days, week off, paid days, leaves, holidays, absent) of perticular month.',
    'description': """
                    Employee Attendances Muster
                    Employee Attendace Dashboard
                    Employee Attendance
                    Attendance Dashboard
            """,
    'author':'Preciseways',
    'category': 'Generic Modules/Human Resources',
    'website': "http://www.preciseways.com",
    'depends':['hr_attendance', 'hr_holidays', 'hr_work_entry_contract'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_attendance_dashboard_view.xml',
        'views/res_config_settings_view.xml',
        'views/hr_employee_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pways_attendance_muster/static/src/js/atttendance_dashbord.js',
            'pways_attendance_muster/static/src/css/attendance_dashboard.css',
        ],
        'web.assets_qweb': [
            'pways_attendance_muster/static/src/xml/attendance_dashboard.xml',
        ],
    },
    'installable': True,
    'application': True,
    'price': 35.0,
    'currency': 'EUR',
    'images':['static/description/banner.png'],
    'license': 'LGPL-3',
}
