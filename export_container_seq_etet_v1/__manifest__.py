{
    'name': 'Consecutivos contenedor',
    'version': '0.1',
    'summary': 'Summery',
    'description': 'Consecutivos contenedor por cliente',
    'category': 'Category',
    'author': 'Cesar Quiroga',
    'website': 'Website',
    'depends': ['base', 'sale','contacts','stock' ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_views.xml',
        'views/res_partner_views.xml',
        'views/containers_views.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False
}