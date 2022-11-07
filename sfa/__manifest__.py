{
<<<<<<< HEAD
    'name': 'SFA',
=======
    'name': 'Cost / Profit Centers',
>>>>>>> production
    'version': '15.0.0.0',
    'category': 'Accounting',
    'summary': '',
    'description': """""",
    'author': 'PlanetOdoo',
<<<<<<< HEAD
    'depends': ['base', 'sale', 'purchase', 'account', 'stock'],
    "data": [
        "security/ir.model.access.csv",
        "wizards/analytic_account_wizard.xml",
        "reports/report.xml",
        "reports/proforma_invoice.xml",
        "reports/salary_slip.xml",
        "views/account.xml",
=======
    'depends': ['base', 'account'],
    "data": [
        "security/ir.model.access.csv",
        "wizards/analytic_account_wizard.xml",
>>>>>>> production
        "views/cost_profit_center.xml",
        "views/location.xml",
        "views/departments.xml",
        "views/sub_departments.xml",
<<<<<<< HEAD
        "views/analytic_account.xml",
        "views/res_view.xml",
        "views/import_vendor_bills_view.xml",
        "views/partner.xml",
        "views/import_contra_voucher.xml",
        "views/import_receipt_register.xml",
        "views/accounting.xml",
        "views/hr_payslip_change.xml",
=======
        "views/analytic_account.xml"
>>>>>>> production
    ],
    "assets": {
        "web.assets_backend": [

        ],
        "web.assets_qweb": [

        ],
    },
    'website': 'https://planet-odoo.com/',
    'installable': True,
    'auto_install': False,
}
