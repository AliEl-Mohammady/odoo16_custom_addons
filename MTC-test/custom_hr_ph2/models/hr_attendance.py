from odoo import fields, models, api, _
import datetime
import math
import pytz
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta, time
from dateutil.relativedelta import relativedelta


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'
 
    department_id = fields.Many2one('hr.department', string='Department', compute='_compute_employee_details', store=True)
    resource_calendar_id = fields.Many2one('resource.calendar', string='Working Hours', compute='_compute_employee_details', store=True)
    employee_shift = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('g1', 'G1'),
        ('g2', 'G2')
    ], string='Employee Shift', store=True, compute='_compute_employee_details')
    emp_id = fields.Char(string='Employee Id', store=True, required=False, compute='_compute_employee_details')

    overtimee_hours = fields.Float(
        string='Overtime Hours', compute='_compute_overtime_hours', store=True, group_operator='sum')
    overtime_amount = fields.Float(
        string='Overtime Amount', compute='_compute_overtime_amount', store=True, group_operator='sum')
    overtime_type = fields.Selection(
        [('single', 'Single Overtime'), ('double', 'Double Overtime')],
        string='Overtime Type', store=True, compute='_compute_overtime_type'
    )

    is_weekend = fields.Boolean(string='Is Weekend?', store=True, compute='_compute_is_weekend')
    shift_hours = fields.Float(string='Shift Hours', store=True, compute='_compute_shift_hours')

    is_holiday = fields.Boolean(string='Is Holiday?', store=True, compute='_compute_is_holiday')
    holiday = fields.Char(string='Holiday', store=True, compute='_compute_is_holiday')

    planned_ch_in = fields.Float(
        string="Planned Check In",
        compute='_compute_planned_ch_in_out',
        readonly=True,
        store=True,
    )

    planned_ch_out = fields.Float(
        string="Planned Check Out",
        compute='_compute_planned_ch_in_out',
        readonly=True,
        store=True,
    )

    date_from = fields.Date(
        string="Start Date",
        compute='_compute_planned_ch_in_out',
        readonly=True,
        store=True,
    )

    date_to = fields.Date(
        string="End Date",
        compute='_compute_planned_ch_in_out',
        readonly=True,
        store=True,
    )

    is_cross_shift = fields.Boolean(string='Is Cross Shift', compute='_compute_shift_hours', store=True)
    overtime_after = fields.Float(string='Overtime After', compute='_compute_shift_hours', store=True)

## Handle Working Times on the Two Cases With and Without Start Date and End Date ##
    @api.depends('employee_id', 'check_in', 'is_cross_shift', 'overtime_after')
    def _compute_planned_ch_in_out(self):
        for attendance in self:
            attendance.planned_ch_in = 0.0
            attendance.planned_ch_out = 0.0
            attendance.date_from = False
        
            if attendance.employee_id and attendance.check_in:
                attendance_date = fields.Datetime.from_string(attendance.check_in).date()
                attendance.date_from = attendance_date
            
                if not attendance.is_cross_shift:
                    dayofweek = str(attendance.check_in.weekday())
                    if attendance.date_from:
                        calendar_attendance = attendance.employee_id.contract_id.resource_calendar_id.attendance_ids.filtered(
                            lambda att: att.dayofweek == dayofweek and (not att.date_from or att.date_from == attendance_date)
                        )
                    else:
                        calendar_attendance = attendance.employee_id.contract_id.resource_calendar_id.attendance_ids.filtered(
                            lambda att: att.dayofweek == dayofweek
                        )
                    if calendar_attendance:
                        attendance.planned_ch_in = calendar_attendance[0].hour_from
                        attendance.planned_ch_out = calendar_attendance[0].hour_to
                else:
                    dayofweek = str(attendance.check_in.weekday())
                    if attendance.date_from:
                        calendar_attendance = attendance.employee_id.contract_id.resource_calendar_id.attendance_ids.filtered(
                            lambda att: att.dayofweek == dayofweek and (not att.date_from or att.date_from == attendance_date)
                        )
                    else:
                        calendar_attendance = attendance.employee_id.contract_id.resource_calendar_id.attendance_ids.filtered(
                            lambda att: att.dayofweek == dayofweek
                        )
                    if calendar_attendance:
                        attendance.planned_ch_in = calendar_attendance[0].hour_from
                        attendance.planned_ch_out = calendar_attendance[0].hour_to + attendance.overtime_after

    @api.depends('employee_id', 'check_in', 'date_from')
    def _compute_shift_hours(self):
        for attendance in self:
            shift_hours = 0.0
            overtime_after = 0.0
            is_cross_shift = False 

            if attendance.employee_id and attendance.check_in:
                attendance_date = fields.Datetime.from_string(attendance.check_in).date()
                contract = self.env['hr.contract'].search([
                    ('employee_id', '=', attendance.employee_id.id),
                    ('resource_calendar_id', '!=', False),
                ], limit=1)
                if contract:
                    resource_calendar = contract.resource_calendar_id
                    dayofweek = str(attendance.check_in.weekday())
                    if attendance.date_from:
                        calendar_attendance = resource_calendar.attendance_ids.filtered(
                            lambda att: att.dayofweek == dayofweek and (not att.date_from or att.date_from == attendance_date)
                        )
                    else:
                        calendar_attendance = resource_calendar.attendance_ids.filtered(
                            lambda att: att.dayofweek == dayofweek
                        )
                    if calendar_attendance:
                        shift_hours = calendar_attendance[0].shift_hours
                        is_cross_shift = calendar_attendance[0].is_cross_shift
                        overtime_after = calendar_attendance[0].overtime_after

            attendance.shift_hours = shift_hours
            attendance.is_cross_shift = is_cross_shift
            attendance.overtime_after = overtime_after
## Handle Working Times the Two Cases With and Without Start Date and End Date ##

#----------------------------------------------------------#

## Handle Attendance on Public Holidays ##
    @api.depends('check_in')
    def _compute_is_holiday(self):
        for attendance in self:
            is_holiday = False
            holiday_name = False

            if attendance.check_in:
                # Look for contract
                contract = self.env['hr.contract'].search([
                    ('employee_id', '=', attendance.employee_id.id),
                    ('state', '=', 'open'),
                ], limit=1)

                if contract:
                    # Look for public holidays defined in resource.calendar.leaves
                    public_holidays = self.env['resource.calendar.leaves'].search([
                        ('date_from', '<=', attendance.check_in),
                        ('date_to', '>=', attendance.check_in),
                    ])

                    # Exclude Time Off types containing "Time Off" in their name
                    excluded_holidays = public_holidays.filtered(lambda h: 'Time Off' in h.name)

                    # If a public holiday is found and it's not a Time Off type, set is_holiday to True and get holiday name
                    if public_holidays and not excluded_holidays:
                        is_holiday = True
                        holiday_name = public_holidays[0].name

            # Set computed values for is_holiday and holiday fields
            attendance.is_holiday = is_holiday
            attendance.holiday = holiday_name
## Handle Attendance on Public Holidays ##

    @api.depends('shift_hours')
    def _compute_is_weekend(self):
        for attendance in self:
            attendance.is_weekend = attendance.shift_hours <= 0                

    day = fields.Selection([
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    ], string='Day', compute='_compute_day', store=True, readonly=True)

    def _get_day_number(self, day):
        """Get the day number for the given day."""
        days = {
            'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4,
            'saturday': 5,
            'sunday': 6,
        }
        return days.get(day, -1)

    @api.depends('check_in')
    def _compute_day(self):
        for attendance in self:
            if attendance.check_in:
                check_in_date = fields.Datetime.from_string(attendance.check_in)
                timezone = attendance.env.user.tz or pytz.utc
                check_in_date = check_in_date.replace(tzinfo=pytz.UTC)
                day_number = check_in_date.weekday()  # Get the day number (0-6) using weekday() method
                attendance.day = str(day_number)  # Convert the day number to string and assign it to attendance.day
            else:
                attendance.day = False

    @api.depends('employee_id', 'worked_hours', 'shift_hours', 'is_weekend')
    def _compute_overtime_hours(self):
        for attendance in self:
            if attendance.worked_hours and attendance.shift_hours:
                attendance.overtimee_hours = attendance.worked_hours - attendance.shift_hours
                attendance.overtimee_hours = max(0.0, attendance.overtimee_hours)
            elif attendance.is_weekend:
                attendance.overtimee_hours = attendance.worked_hours
            else:
                attendance.overtimee_hours = 0.0

    @api.depends('overtimee_hours')
    def _compute_overtime_type(self):
        for attendance in self:
            if attendance.is_weekend == False:
                employee = attendance.employee_id
                if attendance.overtimee_hours > employee.num_hours:
                    attendance.overtime_type = 'double'
                elif attendance.overtimee_hours == 0:
                    attendance.overtime_type = ''
                else:
                    attendance.overtime_type = 'single'
            elif attendance.is_weekend == True:
                employee = attendance.employee_id
                attendance.overtime_type = 'double'

    @api.depends('overtimee_hours', 'overtime_type', 'shift_hours', 'approval_status')
    def _compute_overtime_amount(self):
        for attendance in self:
            if attendance.approval_status == 'approved':
                employee = attendance.employee_id
                if attendance.is_weekend == False:
                    if attendance.overtime_type == 'single':
                        contract = attendance.employee_id.contract_id
                        if contract:
                            calculated_amount = ((contract.wage / 30) / attendance.shift_hours) * (
                                    attendance.overtimee_hours * employee.single_overtime_rate)
                        else:
                            calculated_amount = 0.0
                    elif attendance.overtime_type == 'double':
                        contract = attendance.employee_id.contract_id
                        if contract:
                            calculated_amount = ((contract.wage / 30) / attendance.shift_hours) * (
                                    attendance.overtimee_hours * employee.double_overtime_rate)
                        else:
                            calculated_amount = 0.0
                elif attendance.is_weekend:
                    if attendance.overtime_type == 'single' or attendance.overtime_type == 'double':
                        contract = attendance.employee_id.contract_id
                        if contract:
                            calculated_amount = ((contract.wage / 30) / 8) * (
                                    attendance.overtimee_hours * employee.double_overtime_rate)
                        else:
                            calculated_amount = 0.0
                elif attendance.is_holiday:
                    if attendance.overtime_type == 'single' or attendance.overtime_type == 'double':
                        contract = attendance.employee_id.contract_id
                        if contract:
                            calculated_amount = ((contract.wage / 30) / 8) * (
                                    attendance.overtimee_hours * employee.double_overtime_rate)
                        else:
                            calculated_amount = 0.0
                elif attendance.is_weekend and attendance.is_holiday:
                    if attendance.overtime_type == 'single' or attendance.overtime_type == 'double':
                        contract = attendance.employee_id.contract_id
                        if contract:
                            calculated_amount = ((contract.wage / 30) / 8) * (
                                    attendance.overtimee_hours * employee.double_overtime_rate) * 2
                        else:
                            calculated_amount = 0.0
                    else:
                        calculated_amount = 0.0
                
                attendance.overtime_amount = calculated_amount
            else:
                attendance.overtime_amount = 0.0

    @api.depends('employee_id', 'emp_id')
    def _compute_employee_details(self):
        for attendance in self:
            if attendance._origin:
                continue
            if attendance.employee_id:
                attendance.department_id = attendance.employee_id.department_id.id
                attendance.resource_calendar_id = attendance.employee_id.resource_calendar_id.id
                attendance.employee_shift = attendance.employee_id.employee_shift
                attendance.emp_id = attendance.employee_id.emp_id
            elif attendance.emp_id:
                employee = self.env['hr.employee'].search([('emp_id', '=', attendance.emp_id)], limit=1)
                if employee:
                    attendance.employee_id = employee.id
                    attendance.department_id = employee.department_id.id
                    attendance.resource_calendar_id = employee.resource_calendar_id.id
                    attendance.employee_shift = employee.employee_shift
                else:
                    attendance.department_id = False
                    attendance.resource_calendar_id = False
                    attendance.employee_shift = False
            else:
                attendance.department_id = False
                attendance.resource_calendar_id = False
                attendance.employee_shift = False

#Handle Import Using Excel Sheets:
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'emp_id' in vals and not vals.get('employee_id'):
                employee = self.env['hr.employee'].search([
                    ('emp_id', '=', vals['emp_id'])
                ], limit=1)

                if employee:
                    vals['employee_id'] = employee.id
                    vals['resource_calendar_id'] = employee.resource_calendar_id.id
                else:
                    vals['employee_id'] = False
                    vals['resource_calendar_id'] = False

            elif 'employee_id' in vals and not vals.get('emp_id'):
                employee = self.env['hr.employee'].browse(vals['employee_id'])
                vals['emp_id'] = employee.emp_id if employee else False
                vals['resource_calendar_id'] = employee.resource_calendar_id.id if employee else False

        return super(HrAttendance, self).create(vals_list)

#Approve and Reject Overtime:
    approval_status = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('no_overtime', 'No Overtime'),
    ], string='Approval Status', compute='_compute_approval_status', store=True, readonly=True, copy=False)

    @api.depends('overtimee_hours')
    def _compute_approval_status(self):
        for attendance in self:
            if attendance.overtimee_hours == 0:
                attendance.approval_status = 'no_overtime'
            else:
                attendance.approval_status = 'draft'

    rejection_reason = fields.Text(string='Rejection Reason', copy=False)

    def action_approve_overtime(self):
        for attendance in self:
            if attendance.overtimee_hours > 0:
                attendance.write({
                    'approval_status': 'approved',
                    'rejection_reason': '',
                })
            else:
                raise ValidationError("Cannot approve overtime with hours equal to 0.")

    def action_reject_overtime(self):
        for attendance in self:
            if attendance.overtimee_hours > 0:
                attendance.write({
                    'approval_status': 'rejected',
                    'rejection_reason': 'Enter your rejection reason here',
                })
            else:
                raise ValidationError(_("Cannot reject overtime with hours equal to 0."))

    def unlink(self):
        if not self.env.user.has_group('hr_attendance.group_hr_attendance_manager'):
            raise UserError(_("Deletion for attendances records is not allowed for your user group."))
        
        return super(HrAttendance, self).unlink()