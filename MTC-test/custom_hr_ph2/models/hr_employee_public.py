from odoo import fields, models, api

class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    emp_id = fields.Char("Employee Id", related='employee_id.emp_id')
    children_details = fields.Text(string='Children Details', related='employee_id.children_details')
    insurance_num = fields.Char(string='Number of Insurance', related='employee_id.insurance_num')
    registration_date = fields.Date(string='Registration Date', related='employee_id.registration_date')
    registration_attachment = fields.Binary(string='Registration Attachment', related='employee_id.registration_attachment')

    date_join= fields.Date(string= "Join Date", related='employee_id.date_join')
    military_status = fields.Selection([
        ('exemption_from_military_service', 'Exemption From Military Service'),
        ('temporary_exemption_from_military_service', 'Temporary Exemption From Military Service'),
        ('finish_military_service', 'Finish Military Service'),
        ('other', 'Other')
    ], string='Military Status',related='employee_id.military_status')
    union_card = fields.Selection([
        ('available', 'Available'),
        ('Not_available', 'Not Available')
    ], string='Union Card', related='employee_id.union_card')
    employee_shift = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('g1', 'G1'),
        ('g2', 'G2')
    ], string='Employee Shift', related='employee_id.employee_shift')
    number_of_years = fields.Integer(string="Number of Years", related='employee_id.number_of_years')
    age = fields.Integer(string="Age", related='employee_id.age')

    years_or_age = fields.Boolean(string='Years or Age', related='employee_id.years_or_age')

    single_overtime_rate = fields.Float(string="Single Overtime Rate", related='employee_id.single_overtime_rate')
    double_overtime_rate = fields.Float(string="Double Overtime Rate", related='employee_id.double_overtime_rate')
    num_hours = fields.Float(string="Number of Hours", related='employee_id.num_hours')
    total_overtime_hours = fields.Float(string='Total Overtime Hours', related='employee_id.total_overtime_hours')
    single_overtime_hours = fields.Float(string='Single Overtime Hours', related='employee_id.single_overtime_hours')
    double_overtime_hours = fields.Float(string='Double Overtime Hours', related='employee_id.double_overtime_hours')
    total_overtime_amount = fields.Float(string='Total Overtime Amount', related='employee_id.total_overtime_amount')
    single_overtime_amount = fields.Float(string='Single Overtime Amount', related='employee_id.single_overtime_amount')
    double_overtime_amount = fields.Float(string='Double Overtime Amount', related='employee_id.double_overtime_amount')