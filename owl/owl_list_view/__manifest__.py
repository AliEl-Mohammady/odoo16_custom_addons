# -*- coding: utf-8 -*-
{
    'name' : 'OWL Inherit List View',
    'version' : '1.0',
    'summary': ' List View',
    'sequence': -1,
    'description': """Add Buttons to res partner list view""",
    'category': 'OWL',
    'depends' : ['base', 'web','school_student'],
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/res_partner_inherit.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'owl_list_view/static/src/components/*/*.js',
            'owl_list_view/static/src/components/*/*.xml',
            'owl_list_view/static/src/components/*/*.scss',
        ],
    },
}