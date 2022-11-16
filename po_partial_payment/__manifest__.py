{
    'name': 'PO Partial Payment',
    'sequence': 1,
    'category': 'Accounting',
    'description': 'This module helps to reconcile Partial Payments',
    'website': 'https://www.planet-odoo.com/',
    'author': 'Planet Odoo',
    'depends': ['account', 'sale', 'purchase',],
    'data': [
        "security/ir.model.access.csv",
        "views/payment.xml",
        "views/account_move.xml",
        ],
    'installable': True,
    'application': True,
    'license': 'OEEL-1',
}

