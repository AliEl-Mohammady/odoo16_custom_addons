# -*- coding: utf-8 -*-
{
    'name' : 'OWL POS Control Buttons visibility',
    'version' : '1.0',
    'summary': 'POS Control Buttons',
    'sequence': -1,
    'description': """Add Buttons to Pos view""",
    'category': 'OWL',
    'depends' : ['base', 'web','point_of_sale'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/pos_config_inherit.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'point_of_sale.assets': [
            'pos_config_control_buttons/static/src/components/**/*.js',
            'pos_config_control_buttons/static/src/components/**/*.xml',
        ]
    },
}