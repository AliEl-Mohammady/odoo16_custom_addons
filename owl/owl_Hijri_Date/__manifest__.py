# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "OWL Hijri Date",
    'version': '1.2',
    'category': '',
    'summary': 'Object widget library',
    'description': 'Widgets: OWL provides a variety of widgets for displaying data, capturing user input, and interacting'
                   ' with Odoo models. Examples include form fields, buttons, lists, trees, kanban boards, and many others',
    'depends': [ 'sale', 'web', 'base'],
    'data': [
        "views/sale_order_inherit.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'owl_Hijri_Date/static/src/components/**/*.js',
            'owl_Hijri_Date/static/src/components/**/*.xml',
            'owl_Hijri_Date/static/src/components/**/*.scss',
        ],
    },

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
