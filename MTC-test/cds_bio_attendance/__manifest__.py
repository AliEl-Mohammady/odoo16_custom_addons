# -*- coding: utf-8 -*-
{
    'name': "Biometric Attendance Download",

    'summary': """
        """,

    'description': """
    """,

    'author': "Eng.Ramadan Khalil",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'hr_attendance'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'data/data.xml',
        'views/hr_attendance.xml',
        'views/biometric_view.xml',
        'wizard/schedule_wizard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
