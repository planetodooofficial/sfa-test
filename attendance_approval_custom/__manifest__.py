#-*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2022 DHRUV RADADIYA
#
##############################################################################

{
    'name': 'Attendance Approval',
    'version': '15.0.1.0',
    'price': 8.72,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'category': 'Human Resources/Attendances',
    'summary':  """This app allows your user to approve workflow on Attendance.""",
    'description': """This app allows your user to approve reject workflow on Attendance.""",
    'author': 'Dhruv Radadiya',
    'license': 'OPL-1',
    'website': '',
    'images': ['static/description/9.png'],
    'depends': ['hr_attendance',],
    'data': ['security/ir.model.access.csv',
             'wizard/hr_attendance_refuse_wizard_view.xml',
             'wizard/hr_attendance_approve_wizard_view.xml',
             'views/hr_attendance_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

