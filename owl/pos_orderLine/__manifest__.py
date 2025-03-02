# -*- coding: utf-8 -*-
{
    'name' : 'OWL POS OrderLine',
    'version' : '1.0',
    'summary': 'POS OrderLine',
    'sequence': -1,
    'description': """Add Buttons to Pos view""",
    'category': 'OWL',
    'depends' : ['base', 'web','point_of_sale','hr'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/pos_order_inherit.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'point_of_sale.assets': [
            'pos_orderLine/static/src/components/PosOrderline/*.xml',
            'pos_orderLine/static/src/components/PosOrderline/*.js',
            'pos_orderLine/static/src/components/setEmployeesPopup/*.xml',
            'pos_orderLine/static/src/components/setEmployeesPopup/*.js',
            'pos_orderLine/static/src/components/**/*.scss',
        ],
    },
}