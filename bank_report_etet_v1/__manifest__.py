# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Reporte Pago Bancos',
    'version': '1.0',
    'summary': 'summary',
    'description': "reporte generado en excel para pago en entidad financiera",
    'website': 'https://www.endtoendt.com',
    'depends': ['account'],
    'category': 'category',
    'author': 'Cesar Quiroga y Enrrique Aguiar',
    'sequence': 13,
    'demo': [
        
    ],
    'data': [

        'views/bank_report_view.xml',
        'views/res_bank_view.xml',
        'views/res_partner_bank_view.xml',
        'views/res_partner_view.xml',

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,

}
