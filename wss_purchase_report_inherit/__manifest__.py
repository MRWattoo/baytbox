{
    'name': 'Purchase Report Inherit',
    'version': '17.0',
    'category': 'Extra Tools',
    'summary': 'Module to Inherit Purchase Report  ',
    'sequence': '1',
    'license': 'AGPL-3',
    'author': 'Mohsan Raza',
    'Maintainer': 'WSS',
    'website': '',
    'depends': ['purchase','account'], 
    'demo': [],
    'data': [
        'reports/purchase_report.xml',
        'views/purchase_order.xml',
        'views/account_move.xml',
    ],

    'installable': True,
    'application': True,
    'auto install': False,
}
