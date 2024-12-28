import csv
from datetime import datetime, timedelta
import base64


from odoo import models, fields, api,_
from odoo.exceptions import UserError,ValidationError
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "%H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    total_attendance_days = fields.Integer(string='', required=False, compute='_compute_total_attendance_days')

    @api.depends('employee_id')
    def _compute_total_attendance_days(self):
        for rec in self:
            rec.total_attendance_days = int(
                self.env['hr.attendance'].search_count([('employee_id', '=', rec.employee_id.id)]))
