# -*- coding: utf-8 -*-
{
    'name': "Custom HR Phase 2",

    'author': "Bola Ayman",

    'version': '16.0.0.1',
    
    'license': 'AGPL-3',

    'depends': ['base', 'hr', 'hr_attendance', 'calendar', 'resource', 'hr_contract', 'hr_holidays', 'hr_payroll'],

    'data': [
        'views/hr_attendance.xml',
        'views/hr_employee.xml',
        'views/hr_employee_public.xml',
        'views/hr_leave_type.xml',
        'views/hr_leave.xml',
        'views/hr_leave_allocation.xml',
        'views/resource_calendar.xml',
        # 'data/hr_payroll_data.xml',
        ],

}