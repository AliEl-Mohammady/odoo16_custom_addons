# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "OWL KPI",
    'version': '1.2',
    'category': '',
    'summary': 'Object widget library',
    'description': 'Widgets: OWL provides a variety of widgets for displaying data, capturing user input, and interacting'
                   ' with Odoo models. Examples include form fields, buttons, lists, trees, kanban boards, and many others',
    'depends': ['board', 'sale', 'web', 'base'],
    'data': [
        "views/sales_dashboard.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'owl/static/src/components/**/*.js',
            'owl/static/src/components/**/*.xml',
            'owl/static/src/components/**/*.scss',
        ], },

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
