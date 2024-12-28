from odoo import fields, models, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta, time


class HrPayslipWorkedDays(models.Model):
    _inherit = 'hr.payslip'

    def _get_worked_day_lines_values(self, domain=None):
        res = super(HrPayslipWorkedDays, self)._get_worked_day_lines_values(domain=None)
        attendances_days = self.env['hr.attendance'].search_count([('employee_id', '=', self.employee_id.id),('date_from', '>=', self.date_from),('date_from', '<=', self.date_to),])
        print(attendances_days)
        print(res)
        if res != []:
            res[0]['number_of_days'] = int(attendances_days)
        return res
