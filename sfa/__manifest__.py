{
    'name': 'SFA',
    'version': '15.0.0.0',
    'category': 'Accounting',
    'summary': '',
    'description': """""",
    'author': 'PlanetOdoo',
    'depends': ['base', 'sale', 'purchase', 'account', 'stock'],
    "data": [
        "security/ir.model.access.csv",
        "wizards/analytic_account_wizard.xml",
        "views/hr_payslip_change.xml",
        "reports/report.xml",
        "reports/proforma_invoice.xml",
        "reports/salary_slip.xml",
        "views/account.xml",
        "views/cost_profit_center.xml",
        "views/location.xml",
        "views/departments.xml",
        "views/sub_departments.xml",
        "views/analytic_account.xml",
        "views/res_view.xml",
        "views/import_vendor_bills_view.xml",
        "views/partner.xml",
        "views/import_contra_voucher.xml",
        "views/import_receipt_register.xml",
        "views/accounting.xml",

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
