{
    'name': 'Shipping Fee',
    'version': '17.0',
    'category': 'Custom',
    'module_type': 'official',
    'summary': 'Module for Shipping Fee',
    'sequence': '-10009',
    'license': 'AGPL-3',
    'author': 'Hasnain Jutt',
    'Maintainer': 'Hasnain Jutt',
    'website': 'https://www.baytbox.com',
    'depends': [
        'product', 'sale', 'delivery'],
    'demo': [],
    'data': [
        'views/product_category.xml',
        'views/sale_order.xml',
    ],
    'installable': True,
    'application': True,
    'auto install': False,
}
