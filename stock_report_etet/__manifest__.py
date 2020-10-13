# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Inventory Report etet',
    'version': '1.0',
    'summary': 'Manage your stock and logistics activities',
    'description': "",
    'website': 'https://www.endtoendt.com',
    'depends': ['product', 'stock'],
    'category': 'Operations/Inventory',
    'sequence': 13,
    'demo': [
        
    ],
    'data': [

        'wizard/stock_uom_report_view.xml',

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,

}
