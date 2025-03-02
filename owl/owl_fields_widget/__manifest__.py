# -*- coding: utf-8 -*-
{
    'name' : 'OWL Fields Widget',
    'version' : '1.0',
    'summary': 'Fields Widget',
    'sequence': -1,
    'description': """valid email and dynamic field""",
    'category': 'OWL',
    'depends' : ['base', 'web'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_partner_inherit.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'owl_fields_widget/static/src/components/*/*.js',
            'owl_fields_widget/static/src/components/*/*.xml',
            'owl_fields_widget/static/src/components/*/*.scss',
        ],
    },
}