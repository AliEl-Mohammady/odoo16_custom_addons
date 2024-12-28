# -*- coding: utf-8 -*-
{
    'name': "School Student",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Ali Mohamed",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'school','contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/hobby.csv',
        'data/school.student.csv',
        'data/student_data.xml',
        'data/delete_tag.xml',
        'wizard/student_fees_update_wizard.xml',
        'views/views.xml',
        'views/templates.xml',
        'data/student_noupdate_example.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
