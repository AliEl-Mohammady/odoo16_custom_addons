from odoo import fields, models, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta, time


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    department_id = fields.Many2one('hr.department', tracking=True)
    children_details = fields.Text(string='Children Details', tracking=True, store=True)
    identification_id = fields.Char(tracking=True)
    passport_id = fields.Char(tracking=True)
    insurance_num = fields.Char(string='Number of Insurance', tracking=True, store=True)
    registration_date = fields.Date(string='Registration Date', tracking=True, store=True)
    registration_attachment = fields.Binary(string='Registration Attachment', tracking=True, store=True)

    @api.constrains('identification_id')
    def _check_identification_id(self):
        for record in self:
            if record.identification_id:
                if not record.identification_id.isdigit() or len(record.identification_id) != 14:
                    raise ValidationError("Identification ID must be a 14-digit number.")

#Check the active and archived employees:
    @api.constrains('identification_id')
    def _check_identification_id_unique(self):
        for record in self:
            if record.identification_id:
                domain = [
                    ('identification_id', '=', record.identification_id),
                    '|', ('active', '=', True), ('active', '=', False)
                ]
                existing_employees = self.env['hr.employee'].search(domain)
                if len(existing_employees) > 1 or (len(existing_employees) == 1 and existing_employees != record):
                    raise ValidationError("Identification ID must be unique.")

    @api.constrains('passport_id')
    def _check_passport_id_unique(self):
        for record in self:
            if record.passport_id:
                domain = [
                    ('passport_id', '=', record.passport_id),
                    '|', ('active', '=', True), ('active', '=', False)
                ]
                existing_employees = self.env['hr.employee'].search(domain)
                if len(existing_employees) > 1 or (len(existing_employees) == 1 and existing_employees != record):
                    raise ValidationError("Passport ID must be unique.")

    date_join= fields.Date(
        string= "Join Date",
        required = True,
        tracking=True,
        default=lambda self: fields.Date.today()
    )

    military_status = fields.Selection([
        ('exemption_from_military_service', 'Exemption From Military Service'),
        ('temporary_exemption_from_military_service', 'Temporary Exemption From Military Service'),
        ('finish_military_service', 'Finish Military Service'),
        ('other', 'Other')
    ], string='Military Status', store=True, tracking=True, copy=False)

    @api.onchange('gender')
    def _onchange_gender(self):
        self.military_status = False

    union_card = fields.Selection([
        ('available', 'Available'),
        ('Not_available', 'Not Available')
    ], string='Union Card', store=True, tracking=True)

    employee_shift = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('g1', 'G1'),
        ('g2', 'G2')
    ], string='Employee Shift', store=True, tracking=True)

    number_of_years = fields.Integer(compute="_compute_years", string="Number of Years")

    age = fields.Integer(compute="_compute_age", string="Age")
    
    @api.depends("date_join")
    def _compute_years(self):
        for record in self:
            number_of_years = 0
            if record.date_join:
                number_of_years = relativedelta(fields.Date.today(), record.date_join).years
            record.number_of_years = number_of_years

    @api.depends("birthday")
    def _compute_age(self):
        for record in self:
            age = 0
            if record.birthday:
                age = relativedelta(fields.Date.today(), record.birthday).years
            record.age = age