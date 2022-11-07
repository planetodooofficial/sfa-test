{
    'name': 'Employee Tax Declaration',
    'version': '15',
    'summary': 'Employee custom Tax Declaration',
    'sequence': 10,
    'description': """Employee custom Tax Declaration""",
    'depends': [
        'base', 'hr', 'account', 'website',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_tax_declaration_view.xml',
        'views/employee_inherit_view.xml',
        'views/portal_view.xml',
    ],

    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
