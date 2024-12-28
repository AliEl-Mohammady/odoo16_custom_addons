from odoo import fields, models, api, _
from datetime import datetime, time, timedelta
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    emp_id = fields.Char("Employee Id", related='employee_id.emp_id', readonly=True)
    name = fields.Char(required=True)

# Dynamically Get Leaves After Number of months:
    @api.constrains('request_date_from', 'holiday_status_id')
    def _check_date_join(self):
        for leave in self:
            employee = leave.employee_id
            min_months_required = leave.holiday_status_id.minimum_months_required
            if employee.date_join and min_months_required:
                difference = relativedelta(leave.request_date_from, employee.date_join)
                if difference.months < min_months_required:
                    raise ValidationError(_("You cannot request this type of leave before completing %s month(s)." % min_months_required))

# Limit Leaves Per Month:
    @api.constrains('request_date_from', 'holiday_status_id')
    def _check_leave_quota(self):
        for leave in self:
            max_days_per_month = leave.holiday_status_id.max_days_per_month
            if max_days_per_month:
                # Calculate the start and end of the month for the requested leave
                request_month_start = leave.request_date_from.replace(day=1)
                request_month_end = (request_month_start + relativedelta(months=1, days=-1))

                # Calculate the number of days requested by the employee for the month of the leave
                employee_id = leave.employee_id.id
                leave_type_id = leave.holiday_status_id.id
                requested_leave_days = sum(leave.number_of_days for leave in self.env['hr.leave'].search([
                    ('employee_id', '=', employee_id),
                    ('holiday_status_id', '=', leave_type_id),
                    ('state', 'in', ['confirm', 'validate1', 'validate']),
                    ('request_date_from', '>=', request_month_start),
                    ('request_date_to', '<=', request_month_end)
                ]))

                # Check if the requested days exceed the allowed quota
                if requested_leave_days > max_days_per_month:
                    raise ValidationError(_("You cannot request more than %s days of this type of leave in a month." % max_days_per_month))