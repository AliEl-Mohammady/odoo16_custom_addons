from odoo import models, fields, api
from datetime import datetime, timedelta

class HrLeaveAllocation(models.Model):
    _inherit = 'hr.leave.allocation'

    note = fields.Char(string="Note", compute='_compute_note')
    emp_id = fields.Char("Employee Id", related='employee_id.emp_id', readonly=True)
    
    @api.depends('employee_id.number_of_years', 'employee_id.age')
    def _compute_note(self):
        for allocation in self:
            if allocation.employee_id.number_of_years >= 10 and allocation.employee_id.age < 50:
                allocation.note = "This employee has been working with us for {} years.".format(allocation.employee_id.number_of_years)
            elif allocation.employee_id.age >= 50 and allocation.employee_id.number_of_years < 10:
                allocation.note = "The age of this employee is {} years.".format(allocation.employee_id.age)
            elif allocation.employee_id.age >= 50 and allocation.employee_id.number_of_years >= 10:
                allocation.note = "This employee has been working with us for {} years and is {} years old.".format(allocation.employee_id.number_of_years, allocation.employee_id.age)
            else:
                allocation.note = False

    @api.onchange('holiday_status_id', 'date_from')
    def _compute_allocation_days(self):
        for record in self:
            if record.holiday_status_id and record.date_from:
                holiday_days = record.holiday_status_id.holiday_days
                start_date = fields.Date.from_string(record.date_from)
                end_date = fields.Date.from_string(record.date_from.replace(year=start_date.year, month=12, day=31))

                delta = end_date - start_date
                record.number_of_days = delta.days * (holiday_days / 365)

    @api.model
    def create(self, values):
        if 'date_from' in values and 'holiday_status_id' in values:
            holiday_status = self.env['hr.leave.type'].browse(values['holiday_status_id'])
            if holiday_status:
                date_from = values['date_from']
                values['date_to'] = False

        return super(HrLeaveAllocation, self).create(values)

    def write(self, values):
        if 'date_from' in values and 'holiday_status_id' in values:
            holiday_status = self.env['hr.leave.type'].browse(values['holiday_status_id'])
            if holiday_status:
                date_from = values['date_from']
                values['date_to'] = False

        return super(HrLeaveAllocation, self).write(values)