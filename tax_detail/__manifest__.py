{
    'name': 'Tax Detail',
    'version': '1.0',
    'summary': "Module to show the detail of taxes in a purchase order Odoo version 13",
    'description': """Module to show the detail of taxes in a purchase order Odoo version 13""",
    'category': 'Purchase Management',
    'author': "Jvaldesb - Kiware.co",
    'website': "https://kiware.co",
    'depends': ['base', 'account', 'purchase'],
    'data': [
        #'security/ir.model.access.csv',
        "views/purchase_views.xml"
    ],
    'installable': True,
    'auto_install': False
}
