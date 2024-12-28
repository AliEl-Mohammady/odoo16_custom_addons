from odoo import fields, models, api
import datetime
import math
import pytz
from odoo.exceptions import ValidationError
from datetime import datetime, date, timedelta, time
from dateutil.relativedelta import relativedelta

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    single_overtime_rate = fields.Float(string="Single Overtime Rate", tracking=True)
    double_overtime_rate = fields.Float(string="Double Overtime Rate", tracking=True)
    num_hours = fields.Float(string="Number of Hours", tracking=True)
    
    total_overtime_hours = fields.Float(string='Total Overtime Hours', compute='_compute_total_overtime_hours')
    single_overtime_hours = fields.Float(string='Single Overtime Hours', compute='_compute_total_separate_overtime_hours')
    double_overtime_hours = fields.Float(string='Double Overtime Hours', compute='_compute_total_separate_overtime_hours')

    @api.depends('attendance_ids', 'attendance_ids.overtimee_hours', 'attendance_ids.overtime_type')
    def _compute_total_separate_overtime_hours(self):
        for employee in self:
            current_month_attendances = employee.attendance_ids.filtered(
                lambda att: att.check_in.month == fields.Date.today().month
            )
            single_overtime_attendances = current_month_attendances.filtered(lambda att: att.overtime_type == 'single')
            double_overtime_attendances = current_month_attendances.filtered(lambda att: att.overtime_type == 'double')
            employee.single_overtime_hours = sum(single_overtime_attendances.mapped('overtimee_hours'))
            employee.double_overtime_hours = sum(double_overtime_attendances.mapped('overtimee_hours'))

    @api.depends('attendance_ids', 'attendance_ids.overtimee_hours')
    def _compute_total_overtime_hours(self):
        for employee in self:
            current_month_attendances = employee.attendance_ids.filtered(
                lambda att: att.check_in.month == fields.Date.today().month
            )
            employee.total_overtime_hours = sum(current_month_attendances.mapped('overtimee_hours'))


    total_overtime_amount = fields.Float(string='Total Overtime Amount', compute='_compute_total_overtime_amount')
    single_overtime_amount = fields.Float(string='Single Overtime Amount', compute='_compute_total_separate_overtime_amount')
    double_overtime_amount = fields.Float(string='Double Overtime Amount', compute='_compute_total_separate_overtime_amount')


    @api.depends('attendance_ids', 'attendance_ids.overtime_amount')
    def _compute_total_overtime_amount(self):
        for employee in self:
            current_month_attendances = employee.attendance_ids.filtered(
                lambda att: att.check_in.month == fields.Date.today().month
            )
            employee.total_overtime_amount = sum(current_month_attendances.mapped('overtime_amount'))

    @api.depends('attendance_ids', 'attendance_ids.overtimee_hours', 'attendance_ids.overtime_type')
    def _compute_total_separate_overtime_amount(self):
        for employee in self:
            current_month_attendances = employee.attendance_ids.filtered(
                lambda att: att.check_in.month == fields.Date.today().month
            )
            single_overtime_attendances = current_month_attendances.filtered(lambda att: att.overtime_type == 'single')
            double_overtime_attendances = current_month_attendances.filtered(lambda att: att.overtime_type == 'double')
            employee.single_overtime_amount = sum(single_overtime_attendances.mapped('overtime_amount'))
            employee.double_overtime_amount = sum(double_overtime_attendances.mapped('overtime_amount'))


    overtime_type_counts = fields.Integer(string='Overtime Counts', compute='_compute_overtime_type_counts')
    single_overtime_count = fields.Integer(string='Single Overtime Count', compute='_compute_separated_overtime_type_counts')
    double_overtime_count = fields.Integer(string='Double Overtime Count', compute='_compute_separated_overtime_type_counts')


    @api.depends('attendance_ids', 'attendance_ids.overtime_type')
    def _compute_separated_overtime_type_counts(self):
        for employee in self:
            current_month_attendances = employee.attendance_ids.filtered(
                lambda att: att.check_in.month == fields.Date.today().month
            )
            separated_overtime_type_counts = {
                'single': 0,
                'double': 0
            }
            for attendance in current_month_attendances:
                if attendance.overtime_type == 'single':
                    separated_overtime_type_counts['single'] += 1
                elif attendance.overtime_type == 'double':
                    separated_overtime_type_counts['double'] += 1
            employee.single_overtime_count = separated_overtime_type_counts['single']
            employee.double_overtime_count = separated_overtime_type_counts['double']

    @api.depends('single_overtime_count', 'double_overtime_count')
    def _compute_overtime_type_counts(self):
        for employee in self:
            employee.overtime_type_counts = employee.single_overtime_count + employee.double_overtime_count

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-Cron Job (Scheduled Actions)-#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

#Scheduled Action For Employees who become 50 years or more or worked for 10 years or more:
    years_or_age = fields.Boolean(string='Years or Age', help='The value of this field is set to true only if (Employee age is greater than or equal 50 years based on date of birth) or (Number of years is greater than or equal 10 years based on join date)', store=True, readonly=True, copy=False)

    def check_employee_age_and_years(self):
        employee_ids = self.search([])
        for rec in employee_ids:
            if rec.age and rec.age >= 50 or rec.number_of_years and rec.number_of_years >=10:
                rec.years_or_age = True