# -*- coding: utf-8 -*-
{
    'name': "Hook Examples",

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
    'depends': ['contacts'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/student_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'pre_init_hook': '_first_pre_init_hook',
    'post_init_hook': '_second_post_init_hook',
    'uninstall_hook': '_thierd_uninstall_hook',
    'post_load': '_post_load_hook',
}