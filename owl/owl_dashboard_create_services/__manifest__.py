# -*- coding: utf-8 -*-
{
    'name' : 'OWL Dashboard',
    'version' : '1.0',
    'summary': 'OWl Dashboard App',
    'sequence': -1,
    'description': """owl framework""",
    'category': 'OWL',
    'depends' : ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/odoo_dashboard.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'owl_dashboard_create_services/static/src/components/*/*.js',
            'owl_dashboard_create_services/static/src/components/*/*.xml',
            'owl_dashboard_create_services/static/src/components/*/*.scss',
        ],
    },
}