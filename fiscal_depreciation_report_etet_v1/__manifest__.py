# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Reporte Depreciacion Fiscal',
    'version': '1.0',
    'summary': 'summary',
    'description': "reporte activos fijos",
    'website': 'https://www.endtoendt.com',
    'depends': ['account','account_asset'],
    'category': 'category',
    'author': 'Enrrique Aguiar',
    'sequence': 13,
    'demo': [
        
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/fiscal_depreciation_report_view.xml',
        'views/account_asset_form_view.xml',


    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,

}
