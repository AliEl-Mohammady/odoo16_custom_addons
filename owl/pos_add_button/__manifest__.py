# -*- coding: utf-8 -*-
{
    'name' : 'OWL POS Add Button',
    'version' : '1.0',
    'summary': 'POS Add Button',
    'sequence': -1,
    'description': """Add Buttons to Pos view""",
    'category': 'OWL',
    'depends' : ['base', 'web','point_of_sale'],
    'data': [
        # 'security/ir.model.access.csv',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'point_of_sale.assets': [
            'pos_add_button/static/src/components/**/*.js',
            'pos_add_button/static/src/components/**/*.xml',
        ]
    },
}