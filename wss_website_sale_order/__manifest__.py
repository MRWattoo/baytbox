# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Sale Inherit Odoo',
    'version': '17.0',
    'category': 'Studio',
    'module_type': 'official',
    'summary': '',
    'description': """ """,
    'price': 000,
    'currency': 'EUR',
    'author': 'Mohsan Raza',
    'website': 'wattoosoft.com',
    'depends': ['base', 'website_sale','product','wss_res_country','sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_city.xml',
        'views/product_product.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'wss_website_sale_order/static/src/css/*.css',
            'wss_website_sale_order/static/src/scss/*.scss',
            # 'wss_website_sale_order/static/src/js/product.js',
        ],
    },

    'installable': True,
    'auto_install': False,
}

