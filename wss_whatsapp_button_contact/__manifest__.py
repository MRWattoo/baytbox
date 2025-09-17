{
    'name': 'Whatsapp Button',
    'version': '17.0',
    'category': 'Extra Tools',
    'summary': 'Module to add Whatsapp Button on Contacts',
    'sequence': '1',
    'license': 'AGPL-3',
    'author': 'Mohsan Raza',
    'Maintainer': 'WSS',
    'website': '',
    'depends': ['contacts'
],
    'demo': [],
    'data': [
        'views/res_partner.xml',
# '/static/src/xml/whatsapp_button_template.xml'
    ],
    # 'assets': {
    #     'web.assets_qweb': [
    #         'static/src/xml/whatsapp_button_template.xml'],
    #     'web.assets_backend': [
    #         'static/src/js/whatsapp_button_widget.js'],
    # },

    # 'qweb': ['/static/src/xml/whatsapp_button_template.xml'],
    # 'js': ['/static/src/js/whatsapp_button_widget.js'],
    # 'assets': {
    # #     'web.assets_qweb': [
    # #         '/static/src/xml/whatsapp_button_template.xml',
    # #     ],
    # #     'web.assets_backend': [
    # #         '/static/src/xml/whatsapp_button_template.xml',
    # #         '/static/src/js/whatsapp_button_widget.js',  # Register as a field widget
    # #     ],
    #     'qweb': ['/static/src/xml/whatsapp_button_template.xml'],
    #     'js': ['/static/src/js/whatsapp_button_widget.js'],
    #         'web.assets_common': [
    #
    #             '/static/src/js/whatsapp_button_widget.js',
    #         ],
    #
    # },




    # 'assets': {
    #     # 'web.assets_backend': [
    #     #     # '/static/src/xml/whatsapp_button_template.xml',
    #     #     '/static/src/js/whatsapp_button_widget.js',
    #     # ],
    #     # 'web.assets_frontend': [
    #     #     '/static/src/xml/whatsapp_button_template.xml',
    #     # #     'static/src/js/whatsapp_button_widget.js',
    #     # ],
    #     # 'web.assets_common': [
    #     #
    #     #     '/static/src/js/whatsapp_button_widget.js',
    #     # ],
    #
    # },
    #
    'installable': True,
    'application': True,
    'auto install': False,
}
