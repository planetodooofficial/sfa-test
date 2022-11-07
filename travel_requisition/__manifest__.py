{
    'name': 'Travel Requisition Expense',
    'version': '1.1',
    'summary': 'Travel Requisition Expense',
    'sequence': 10,
    'description': """Travel Requisition Expense""",
    'depends': [
        'base', 'hr_expense', 'product', 'website', 'portal', 'hr','l10n_in_hr_payroll','website','portal'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/travel_requisition_views.xml',
        'views/travel_requisition_portal_view.xml',
        'views/employee_fields_view.xml',
        'views/master_data.xml',
        'views/my_reimbursement_portal_view.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
