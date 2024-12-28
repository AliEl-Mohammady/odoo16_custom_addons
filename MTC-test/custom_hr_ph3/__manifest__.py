# -*- coding: utf-8 -*-
{
    'name': "Custom HR Phase 3",

    'author': "Bola Ayman",

    'version': '16.0.0.1',
    
    'license': 'AGPL-3',

    'depends': ['base', 'hr', 'hr_attendance', 'calendar', 'resource', 'hr_contract', 'hr_holidays', 'hr_payroll'],

    'data': [
        'views/hr_employee.xml',
        'views/hr_salary_attachment.xml',
        'views/res_config_settings.xml',
        'data/hr_payroll_data.xml',
        # 'data/hr_work_entry_type_data.xml',
        ],

}
