# -*- coding: utf-8 -*-
{
    'name' : 'OWL Services',
    'version' : '1.0',
    'summary': 'OWl Services App',
    'sequence': -1,
    'description': """owl framework""",
    'category': 'OWL',
    'depends' : ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/odoo_services.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'owl_services/static/src/components/*/*.js',
            'owl_services/static/src/components/*/*.xml',
            'owl_services/static/src/components/*/*.scss',
        ],
    },
}