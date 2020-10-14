# -*- coding: utf-8 -*-
# Keware.co - Julián Valdés - Info@keware.co / See LICENSE file for full copyright and licensing details.

{
    'name': 'Mass Payment',
    'version': '2.0',
    'summary': "Module to make massive payments of supplier invoices in Odoo version 13 community",
    'description': """Module to make massive payments of supplier invoices in Odoo version 13 community""",
    'category': 'Accounting/Accounting',
    'author': "Jvaldesb - Kiware.co",
    'website': "https://kiware.co",
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'data/payment_data.xml',
        'views/payment_view.xml'
    ],
    'installable': True,
    'auto_install': False
}
