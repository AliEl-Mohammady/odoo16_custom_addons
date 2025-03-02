# -*- coding: utf-8 -*-
{
    'name' : 'OWL Disable Form View',
    'version' : '1.0',
    'summary': 'Disable Form View using OWL App',
    'sequence': -1,
    'description': """""",
    'category': 'OWL',
    'depends' : ['base','sale'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order_inherit.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'owl_disable_form/static/src/components/*/*.js',
            'owl_disable_form/static/src/components/*/*.xml',
            'owl_disable_form/static/src/components/*/*.scss',
        ],
    },
}