# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Reporte Activos Fijos',
    'version': '1.0',
    'summary': 'summary',
    'description': "reporte activos fijos",
    'website': 'https://www.endtoendt.com',
    'depends': ['account'],
    'category': 'category',
    'author': 'Cesar Quiroga y Enrrique Aguiar',
    'sequence': 13,
    'demo': [
        
    ],
    'data': [

        'views/asset_report_view.xml',

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,

}
