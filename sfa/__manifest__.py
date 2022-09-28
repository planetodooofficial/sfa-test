{
    'name': 'Cost / Profit Centers',
    'version': '15.0.0.0',
    'category': 'Accounting',
    'summary': '',
    'description': """""",
    'author': 'PlanetOdoo',
    'depends': ['base', 'account'],
    "data": [
        "security/ir.model.access.csv",
        "wizards/analytic_account_wizard.xml",
        "views/cost_profit_center.xml",
        "views/location.xml",
        "views/departments.xml",
        "views/sub_departments.xml",
        "views/analytic_account.xml"
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
