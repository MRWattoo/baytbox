{
    'name': 'Dropship Statuses',
    'version': '17.0',
    'category': 'Custom',
    'module_type': 'official',
    'summary': 'Module for Dropship Statuses',
    'sequence': '-10009',
    'license': 'AGPL-3',
    'author': 'Hasnain Jutt',
    'Maintainer': 'Hasnain Jutt',
    'website': 'https://www.baytbox.com',
    'depends': [
        'stock', 'sale_stock',
    ],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'views/reason_cancel.xml',
        'views/views.xml',
        'views/customer_view_dropship_states.xml',

    ],
    'installable': True,
    'application': True,
    'auto install': False,
}
