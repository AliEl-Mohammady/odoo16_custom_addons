# -*- coding: utf-8 -*-
{
    'name' : 'Todo List App',
    'version' : '1.0',
    'summary': 'Todo List App',
    'sequence': -1,
    'description': """Todo List App using owl framework""",
    'category': 'OWL',
    'depends' : ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/todo_list.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'todo_app/static/src/components/*/*.js',
            'todo_app/static/src/components/*/*.xml',
            'todo_app/static/src/components/*/*.scss',
        ],
    },
}