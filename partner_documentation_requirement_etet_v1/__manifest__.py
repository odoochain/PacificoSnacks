{
    'name': 'Gestion de documentos partner',
    'version': '0.1',
    'summary': 'Summery',
    'description': 'Maneja el control de documentos que los partner',
    'category': 'Category',
    'author': 'Cesar Quiroga',
    'website': 'Website',
    'depends': ['base','purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/documentation_views.xml',
        'views/required_documentation_views.xml',
        'views/partner_documentation_view.xml',
        'views/partner_view.xml',
        'views/purchase_order_view.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False
}