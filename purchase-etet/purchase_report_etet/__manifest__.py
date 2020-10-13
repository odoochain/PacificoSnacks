# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Purchase Report etet',
    'version': '1.0',
    'summary': 'Manage your purchase',
    'description': "",
    'website': 'https://www.endtoendt.com',
    'depends': ['purchase', 'stock'],
    'category': 'Operations/Purchase',
    'sequence': 13,
    'demo': [
        
    ],
    'data': [

        'report/products_supplier_report.xml',
        'report/report.xml',
        # 'views/products_supplierreport_view.xml',
        'wizard/products_supplier_report_view.xml',
        'security/ir.model.access.csv',

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,

}
