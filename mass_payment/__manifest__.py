{
    'name': 'Mass Payment',
    'version': '1.0',
    'summary': "Module to make massive payments of supplier invoices in Odoo version 13 community",
    'description': """Module to make massive payments of supplier invoices in Odoo version 13 community""",
    'category': 'Purchase Management',
    'author': "Jvaldesb",
    'website': "",
    'depends': ['base', 'account', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'data/payment_data.xml',
        'views/payment_view.xml'
    ],
    'installable': True,
    'auto_install': False
}
