from odoo import fields, models, api
import datetime
import math
from odoo.exceptions import ValidationError
from datetime import datetime, date, timedelta, time
from dateutil.relativedelta import relativedelta

class HrEmployee(models.Model):
    _inherit = 'hr.employee'


#Allowances
# 1- Social Raise Allowance:
    get_social_raise_allowance = fields.Boolean(string='Get Social Raise Allowance', tracking=True)
    social_raise_amount = fields.Float(string='Social Raise Amount', store=True, tracking=True)

    @api.onchange('get_social_raise_allowance')
    def _onchange_get_social_raise_allowance(self):
        if self.get_social_raise_allowance == True:
            self.social_raise_amount = 550.0 
        else:
            self.social_raise_amount = 0

# 2- Shift Allowance:
    get_shift_allowance = fields.Boolean(string='Get Shift Allowance', tracking=True)
    worker_or_security = fields.Selection([
        ('worker', 'Worker'),
        ('security', 'Security')
    ], string="Worker or Security?", tracking=True)

    shift_allowance_amount = fields.Float(string='Shift Allowance Amount', store=True, tracking=True)

    @api.onchange('get_shift_allowance', 'worker_or_security')
    def _onchange_worker_or_security(self):
        for employee in self:
            if employee.get_shift_allowance:
                if employee.worker_or_security == 'worker':
                    employee.shift_allowance_amount = 300.0
                elif employee.worker_or_security == 'security':
                    employee.shift_allowance_amount = 400.0
            else:
                employee.worker_or_security = ''
                employee.shift_allowance_amount = 0.0

# 3- Meal Allowance:
    get_meal_allowance = fields.Boolean(string='Get Meal Allowance', tracking=True)
    employee_grade = fields.Selection([
        ('G1', 'G1'),
        ('G2', 'G2'),
        ('G3', 'G3'),
        ('G4', 'G4'),
        ('G5', 'G5')
    ], string='Employee Grade', tracking=True)
    meal_allowance_amount = fields.Float(string='Meal Allowance Amount', store=True, tracking=True)

    @api.onchange('get_meal_allowance', 'employee_grade')
    def _onchange_get_meal_allowance(self):
        for record in self:
            if record.get_meal_allowance:
                if record.employee_grade:
                    record.meal_allowance_amount = 0
                else:
                    record.meal_allowance_amount = 425
            else:
                record.employee_grade = ''
                record.meal_allowance_amount = 0
  
# 4- Supervisor Allowance:
    get_supervisor_allowance = fields.Boolean(string='Get Supervisor Allowance', tracking=True)
    supervisor_or_supervisor_assistant = fields.Selection([
        ('supervisor', 'Supervisor'),
        ('supervisor_assistant', 'Supervisor Assistant')
    ], string='Supervisor or Supervisor Assistant?', tracking=True)
    supervisor_allowance_amount = fields.Float(string='Supervisor Allowance Amount', store=True, tracking=True)

    @api.onchange('get_supervisor_allowance', 'supervisor_or_supervisor_assistant')
    def _onchange_supervisor_or_supervisor_assistant(self):
        for employee in self:
            if employee.get_supervisor_allowance:
                if employee.supervisor_or_supervisor_assistant == 'supervisor':
                    employee.supervisor_allowance_amount = 250.0
                elif employee.supervisor_or_supervisor_assistant == 'supervisor_assistant':
                    employee.supervisor_allowance_amount = 150.0    
            else:
                employee.supervisor_or_supervisor_assistant = ''
                employee.supervisor_allowance_amount = 0

    @api.onchange('get_supervisor_allowance')
    def _onchange_get_supervisor_allowance(self):
        for employee in self:
            if employee.get_supervisor_allowance:
                if employee.supervisor_or_supervisor_assistant == 'supervisor':
                    employee.supervisor_allowance_amount = 250.0
                elif employee.supervisor_or_supervisor_assistant == 'supervisor_assistant':
                    employee.supervisor_allowance_amount = 150.0    
            else:
                employee.supervisor_allowance_amount = 0

# 5- Spinning Allowance:
    get_spinning_allowance = fields.Boolean(string='Get Spinning Allowance', tracking=True)
    spinning_allowance_amount = fields.Float(string='Spinning Allowance Amount', store=True, tracking=True)

    @api.onchange('get_spinning_allowance')
    def _onchange_get_spinning_allowance(self):
        if self.get_spinning_allowance == True:
            self.spinning_allowance_amount = 400.0 
        else:
            self.spinning_allowance_amount = 0

# 6- Housing Allowance:
    get_housing_allowance = fields.Boolean(string='Get Housing Allowance', tracking=True)
    housing_allowance_amount = fields.Float(string='Housing Allowance Amount', store=True, tracking=True)

    @api.onchange('get_housing_allowance')
    def _onchange_get_housing_allowance(self):
        if self.get_housing_allowance == True:
            self.housing_allowance_amount = 150.0 
        else:
            self.housing_allowance_amount = 0

# 7- Drive Allowance:
    get_drive_allowance = fields.Boolean(string='Get Drive Allowance', tracking=True)
    driver_type = fields.Selection([
        ('regular', 'Regular'),
        ('manager', 'Manager')
    ], string='Driver Type', tracking=True)
    license_type = fields.Selection([
        ('first', 'First'),
        ('second', 'Second'),
        ('third', 'Third'),
        ('private', 'Private')
    ], string='License Type', tracking=True)
    drive_allowance_amount = fields.Float(string='Drive Allowance Amount', compute='_compute_drive_allowance_amount', store=True, tracking=True)
    manager_bonus = fields.Float(string='Manager Bonus', default=100.0, tracking=True)
    total_drive_allowance = fields.Float(string='Total Drive Allowance', compute='_compute_total_drive_allowance', store=True, tracking=True)

    @api.depends('get_drive_allowance', 'driver_type', 'license_type', 'drive_allowance_amount', 'manager_bonus')
    def _compute_drive_allowance_amount(self):
        for record in self:
            if record.get_drive_allowance:
                if record.driver_type == 'regular':
                    if record.license_type == 'first':
                        record.drive_allowance_amount = 250.0
                    elif record.license_type == 'second':
                        record.drive_allowance_amount = 200.0
                    elif record.license_type == 'third':
                        record.drive_allowance_amount = 100.0
                    elif record.license_type == 'private':
                        record.drive_allowance_amount = 0.0
                elif record.driver_type == 'manager':
                    if record.license_type == 'first':
                        record.drive_allowance_amount = 250.0
                    elif record.license_type == 'second':
                        record.drive_allowance_amount = 200.0
                    elif record.license_type == 'third':
                        record.drive_allowance_amount = 100.0
                    elif record.license_type == 'private':
                        record.drive_allowance_amount = 0.0
            else:
                record.driver_type = ''
                record.license_type = ''
                record.drive_allowance_amount = 0.0

    @api.onchange('get_drive_allowance' ,'driver_type')
    def _onchange_driver_type(self):
        for record in self:
            if record.get_drive_allowance:
                if record.driver_type == 'regular':
                    record.manager_bonus = 0.0
                elif record.driver_type == 'manager':
                    record.manager_bonus = 100.0
            else:
                record.manager_bonus = 0.0

    @api.depends('drive_allowance_amount', 'manager_bonus')
    def _compute_total_drive_allowance(self):
        for record in self:
            record.total_drive_allowance = record.drive_allowance_amount + record.manager_bonus

# 8- Supervisor Evaluation Allowance:
    get_monthly_supervisor_eval_allowance = fields.Boolean(string='Get Monthly Supervisor Evaluation Allowance', tracking=True)
    total_supervisor_allowance_before_eval = fields.Float(string='Total Supervisor Allowance Before Evaluation', default=250, tracking=True)
    total_supervisor_allowance_after_eval = fields.Float(string='Total Supervisor Allowance After Evaluation', tracking=True, compute='_compute_total_supervisor_allowance_after_eval', store=True)
    total_supervisor_rate = fields.Float(string='Total Supervisor Rate', tracking=True)

    @api.onchange('get_monthly_supervisor_eval_allowance', 'total_supervisor_rate')
    def _onchange_get_monthly_supervisor_eval_allowance(self):
        for employee in self:
            if employee.get_monthly_supervisor_eval_allowance == True:
                employee.total_supervisor_allowance_before_eval = 250
            else:
                employee.total_supervisor_rate = 0
                employee.total_supervisor_allowance_before_eval = 0

    @api.onchange('total_supervisor_rate', 'total_supervisor_allowance_after_eval')
    def _onchange_total_supervisor_rate(self):
        for employee in self:
            if employee.total_supervisor_rate > 100:
                raise ValidationError("Total Supervisor Rate cannot exceed 100.")

    @api.depends('get_monthly_supervisor_eval_allowance', 'total_supervisor_rate', 'total_supervisor_allowance_before_eval')
    def _compute_total_supervisor_allowance_after_eval(self):
        for employee in self:
            if employee.get_monthly_supervisor_eval_allowance:
                employee.total_supervisor_allowance_after_eval = (employee.total_supervisor_rate / 100) * employee.total_supervisor_allowance_before_eval
            else:
                employee.total_supervisor_allowance_after_eval = 0.0

# 9- Supervisor Assistant Evaluation Allowance:
    get_monthly_supervisor_assistant_eval_allowance = fields.Boolean(string='Get Monthly Supervisor Assistant Evaluation Allowance', tracking=True)
    total_supervisor_assistant_allowance_before_eval = fields.Float(string='Total Supervisor Assistant Allowance Before Evaluation', default=150.0, tracking=True)
    total_supervisor_assistant_allowance_after_eval = fields.Float(string='Total Supervisor Assistant Allowance After Evaluation', tracking=True, compute='_compute_total_supervisor_assistant_allowance_after_eval', store=True)
    total_supervisor_assistant_rate = fields.Float(string='Total Assistant Rate', tracking=True)

    @api.onchange('get_monthly_supervisor_assistant_eval_allowance', 'total_supervisor_assistant_rate')
    def _onchange_get_monthly_supervisor_assistant_eval_allowance(self):
        for employee in self:
            if employee.get_monthly_supervisor_assistant_eval_allowance == True:
                self.total_supervisor_assistant_allowance_before_eval = 150
            else:
                employee.total_supervisor_assistant_rate = 0
                employee.total_supervisor_assistant_allowance_before_eval = 0

    @api.onchange('total_supervisor_assistant_rate')
    def _onchange_total_supervisor_assistant_rate(self):
        for employee in self:
            if employee.total_supervisor_assistant_rate > 100:
                raise ValidationError("Total Supervisor Assistant Rate cannot exceed 100.")

    @api.depends('get_monthly_supervisor_assistant_eval_allowance', 'total_supervisor_assistant_rate', 'total_supervisor_assistant_allowance_before_eval')
    def _compute_total_supervisor_assistant_allowance_after_eval(self):
        for employee in self:
            if employee.get_monthly_supervisor_assistant_eval_allowance:
                employee.total_supervisor_assistant_allowance_after_eval = (employee.total_supervisor_assistant_rate / 100) * employee.total_supervisor_assistant_allowance_before_eval
            else:
                employee.total_supervisor_assistant_allowance_after_eval = 0.0

# 10- Job Nature Allowance:
    get_cleaners_allowance = fields.Boolean(string='Get Cleaners Allowance', tracking=True)
    cleaners_allowance_amount = fields.Float(string='Cleaners Allowance Amount',store=True, tracking=True)

    @api.onchange('get_cleaners_allowance')
    def _onchange_get_cleaners_allowance(self):
        if self.get_cleaners_allowance == True:
            self.cleaners_allowance_amount = 200.0
        else:
            self.cleaners_allowance_amount = 0.0

# 11- Incentive Allowance:
    get_incentive_allowance = fields.Boolean(string='Get Incentive Allowance', tracking=True)
    production_allowance_amount = fields.Float(string='Production Allowance Amount', store=True, default=150.0, tracking=True)
    production_efficiency_rate = fields.Float(string='Production Efficiency Rate', tracking=True)
    production_efficiency_amount = fields.Float(string='Production Efficiency Amount', compute='_compute_production_efficiency_amount', tracking=True)
    total_incentive_allowance_amount = fields.Float(string='Total Incentive Allowance Amount', compute='_compute_total_incentive_allowance_amount', tracking=True)

    @api.onchange('get_incentive_allowance', 'production_efficiency_rate')
    def _onchange_incentive_allowance(self):
        for record in self:
            if not record.get_incentive_allowance:
                record.production_allowance_amount = 0.0
                record.production_efficiency_rate = 0.0
                record.production_efficiency_amount = 0.0
                record.total_incentive_allowance_amount = 0.0
            elif record.production_efficiency_rate is not None:
                record.production_allowance_amount = 150.0
                record._compute_production_efficiency_amount()
                record._compute_total_incentive_allowance_amount()

    @api.depends('production_efficiency_rate')
    def _compute_production_efficiency_amount(self):
        for employee in self:
            if employee.production_efficiency_rate == 90:
                employee.production_efficiency_amount = 150
            elif 90 < employee.production_efficiency_rate < 91:
                employee.production_efficiency_amount = 150
            elif 91 <= employee.production_efficiency_rate < 92:
                employee.production_efficiency_amount = 170
            elif 92 <= employee.production_efficiency_rate < 93:
                employee.production_efficiency_amount = 190
            elif 93 <= employee.production_efficiency_rate < 94:
                employee.production_efficiency_amount = 210
            elif 94 <= employee.production_efficiency_rate < 95:
                employee.production_efficiency_amount = 230
            elif 95 <= employee.production_efficiency_rate < 96:
                employee.production_efficiency_amount = 250
            elif 96 <= employee.production_efficiency_rate < 97:
                employee.production_efficiency_amount = 270
            elif 97 <= employee.production_efficiency_rate < 98:
                employee.production_efficiency_amount = 290
            elif 98 <= employee.production_efficiency_rate < 99:
                employee.production_efficiency_amount = 310
            elif 99 <= employee.production_efficiency_rate < 100:
                employee.production_efficiency_amount = 330
            elif employee.production_efficiency_rate >= 100:
                employee.production_efficiency_amount = 350
            else:
                employee.production_efficiency_amount = 0

    @api.depends('production_efficiency_rate', 'production_allowance_amount', 'production_efficiency_amount')
    def _compute_total_incentive_allowance_amount(self):
        for employee in self:
            employee.total_incentive_allowance_amount = employee.production_allowance_amount + employee.production_efficiency_amount

# 12- Spinning Host Allowance:
    get_spinning_host_allowance = fields.Boolean(string='Get Spinning Host Allowance', tracking=True)
    num_days = fields.Integer(string='Number of Days',store=True, tracking=True)
    spinning_host_allowance = fields.Float(string='Spinning Host Allowance', default=400, tracking=True)
    spinning_host_allowance_amount = fields.Float(string='Spinning Host Allowance Amount', store=True, compute='_compute_spinning_host_allowance_amount', tracking=True)

    @api.onchange('get_spinning_host_allowance')
    def _onchange_get_spinning_host_allowance(self):
        if self.get_spinning_host_allowance:
            self.spinning_host_allowance = 400
            self._compute_spinning_host_allowance_amount()
        else:
            self.num_days = 0
            self.spinning_host_allowance = 0.0
            self.spinning_host_allowance_amount = 0.0

    @api.onchange('num_days', 'spinning_host_allowance')
    def _onchange_num_days_or_spinning_host_allowance(self):
        if self.get_spinning_host_allowance:
            self._compute_spinning_host_allowance_amount()
        else:
            self.spinning_host_allowance_amount = 0.0

    @api.depends('get_spinning_host_allowance', 'num_days', 'spinning_host_allowance')
    def _compute_spinning_host_allowance_amount(self):
        for record in self:
            if record.get_spinning_host_allowance:
                record.spinning_host_allowance_amount = (record.spinning_host_allowance / 30) * record.num_days
            else:
                record.spinning_host_allowance_amount = 0.0
 
# Insurance
    insurance_salary = fields.Float(string="Insurance Salary", tracking=True)

    insurance_salary_after_exempt = fields.Float(
        string='Insurance Salary After Exemption',
        compute='_compute_insurance_salary_after_exempt',
    )    
    employee_share_amount = fields.Float(
        string="Employee Share Amount",
        compute='_compute_employee_share_amount',
    )
    company_share_amount = fields.Float(
        string="Company Share Amount", 
        compute='_compute_company_share_amount',
    )
    amount = fields.Float(
        string="Amount", 
        tracking=True,
    )
    basic_for_emergency_fund = fields.Float(
        string="Basic for Emergency Fund",
        tracking=True,
    )
    emergency_fund_amount = fields.Float(
        string="Emergency Fund Amount", 
        compute='_compute_emergency_fund_amount',
    )

    employee_share_type = fields.Selection(
    [('rate', 'Rate'), ('fixed_amount', 'Fixed Amount')],
    string="Employee Share Type",
    tracking=True,
    )
    
    @api.depends('insurance_salary')
    def _compute_insurance_salary_after_exempt(self):
        for employee in self:
            insurance_exempt_rate = float(
                employee.env['ir.config_parameter'].sudo().get_param('custom_hr.insurance_exempt_rate', default='0.0')
            )
            employee.insurance_salary_after_exempt = employee.insurance_salary * (1 - (insurance_exempt_rate / 100))

    @api.depends('employee_share_type', 'insurance_salary_after_exempt', 'amount')    
    def _compute_employee_share_amount(self):
        for employee in self:
            employee_share_type = employee.employee_share_type
            employee_share_rate = float(
                self.env['ir.config_parameter'].sudo().get_param('custom_hr.employee_share_rate', default='0.0')
            )
            if employee_share_type == 'rate':
                employee.employee_share_amount = employee.insurance_salary_after_exempt * (employee_share_rate / 100)
            elif employee_share_type == 'fixed_amount':
                employee.employee_share_amount = employee.amount
            else:
                employee.employee_share_amount = 0.0


    @api.depends('insurance_salary_after_exempt')
    def _compute_company_share_amount(self):
        for employee in self:
            company_share_rate = float(
                employee.env['ir.config_parameter'].sudo().get_param('custom_hr.company_share_rate', default='0.0')
            )
            employee.company_share_amount = employee.insurance_salary_after_exempt * (company_share_rate / 100)

    @api.depends('basic_for_emergency_fund')
    def _compute_emergency_fund_amount(self):
        for employee in self:
            emergency_fund_rate = float(
                employee.env['ir.config_parameter'].sudo().get_param('custom_hr.emergency_fund_rate', default='0.0')
            )
            employee.emergency_fund_amount = employee.basic_for_emergency_fund * (emergency_fund_rate / 100)

#Taxes
    bonus = fields.Float(string="Bonus", tracking=True)

    total_gross_plus_allowances = fields.Float(
        string="Total Gross and Allowances",
        help='This field calculated by summing Contract Wage and Total Allowances.',
        compute='_compute_total_gross_plus_allowances',
    )

    salary_after_allowances_and_deductions = fields.Float(
        string='Salary After Allowances and Deductions',
        help='This field calculated as follows Contract Wage + Total Allowances - Social Raise Allowance(Exempted Allowance) - Employee Share Amount - Bonus.',
        compute='_compute_salary_after_allowances_and_deductions',
    )

    total_allowances = fields.Float(
        string='Total Allowances',
        compute='_compute_total_allowances',
    )

    exempted_allowances = fields.Float(
        string='Exempted Allowances',
        help='The value of this field reflects from Social Raise Allowance if it exists.',
        compute='_compute_exempted_allowances',
    )

    total_allowances_after_exempt = fields.Float(
        string='Total Allowances After Exempt',
        help='This field is calculated by subtracting the Exempted Allowances from the Total Allowances.',
        compute='_compute_total_allowances_after_exempt',
    )

    @api.depends('contract_id')
    def _compute_total_allowances(self):
        for employee in self:
            if employee.contract_id:
                employee.total_allowances = (employee.shift_allowance_amount + employee.meal_allowance_amount + employee.spinning_host_allowance_amount + employee.spinning_allowance_amount + employee.housing_allowance_amount + employee.total_drive_allowance + employee.supervisor_allowance_amount + employee.total_supervisor_allowance_after_eval + employee.total_supervisor_assistant_allowance_after_eval + employee.social_raise_amount + employee.cleaners_allowance_amount + employee.total_incentive_allowance_amount)
            else:
                employee.total_allowances = 0.0

    @api.depends('contract_id')
    def _compute_total_gross_plus_allowances(self):
        for employee in self:
            if employee.contract_id:
                employee.total_gross_plus_allowances = (employee.contract_id.wage + employee.total_allowances)
            else:
                employee.total_gross_plus_allowances = 0.0


    @api.depends('contract_id', 'social_raise_amount', 'employee_share_amount', 'bonus')
    def _compute_salary_after_allowances_and_deductions(self):
        for employee in self:
            if employee.contract_id:
                employee.salary_after_allowances_and_deductions = (employee.total_gross_plus_allowances - employee.social_raise_amount - employee.employee_share_amount - employee.bonus)
            else:
                employee.salary_after_allowances_and_deductions = 0.0


    @api.depends('contract_id','social_raise_amount')
    def _compute_exempted_allowances(self):
        for employee in self:
            if employee.contract_id:
                employee.exempted_allowances = employee.social_raise_amount
            else:
                employee.exempted_allowances = 0.0

    @api.depends('contract_id', 'total_allowances', 'exempted_allowances')
    def _compute_total_allowances_after_exempt(self):
        for employee in self:
            if employee.contract_id:
                employee.total_allowances_after_exempt = employee.total_allowances - employee.exempted_allowances
            else:
                employee.total_allowances_after_exempt

    monthly_personal_exempted = fields.Float(
        string="Monthly Personal Exempted", 
        compute='_compute_monthly_personal_exempted',
        help='The value of this field comes from dividing the Yearly Personal Exempted by 12.',
    )
            
    def _compute_monthly_personal_exempted(self):
        for employee in self:
            yearly_personal_exempted = float(
                employee.env['ir.config_parameter'].sudo().get_param('custom_hr.yearly_personal_exempted', default='0.0')
            )
            employee.monthly_personal_exempted = yearly_personal_exempted / 12


    monthly_tax_base = fields.Float(
        string="Monthly Tax Base", 
        compute='_compute_monthly_tax_base',
        # help='This value of this field is calculated by subtracting the Monthly Personal Exempted from the Salary After Allowances and Deductions',
    )

    def _compute_monthly_tax_base(self):
        for employee in self:
            employee.monthly_tax_base = employee.salary_after_allowances_and_deductions
            # employee.monthly_tax_base = employee.salary_after_allowances_and_deductions - employee.monthly_personal_exempted

    yearly_tax_base = fields.Float(
        string="Yearly Tax Base", 
        compute='_compute_yearly_tax_base',
        help='The value of this field is calculated by multiplying the Monthly Tax Base by 12 and rounding the result down to the nearest 10.',

    )

    def _compute_yearly_tax_base(self):
        for employee in self:
            yearly_tax_base = employee.monthly_tax_base * 12
            employee.yearly_tax_base = math.floor(yearly_tax_base // 10) * 10

    employee_salary_category = fields.Selection([
        ('1st category', 'First Category'),
        ('2nd category', 'Second Category'),
        ('3rd category', 'Third Category'),
        ('4th category', 'Fourth Category'),
        ('5th category', 'Fifth Category'),
        ('6th category', 'Sixth Category')
    ], string='Employee Salary Category', compute='_compute_employee_salary_category')

    @api.depends('yearly_tax_base')
    def _compute_employee_salary_category(self):
        for employee in self:
            if employee.yearly_tax_base <= 600000:
                employee.employee_salary_category = '1st category'
            elif employee.yearly_tax_base <= 700000:
                employee.employee_salary_category = '2nd category'
            elif employee.yearly_tax_base <= 800000:
                employee.employee_salary_category = '3rd category'
            elif employee.yearly_tax_base <= 900000:
                employee.employee_salary_category = '4th category'
            elif employee.yearly_tax_base <= 1200000:
                employee.employee_salary_category = '5th category'
            else:
                employee.employee_salary_category = '6th category'

    employee_yearly_tax = fields.Float(
        string="Employee Yearly Tax", 
        compute='_compute_employee_yearly_tax',
        help='The value of this field is calculated according to the Tax Bracket to which the employee belongs, based on the Yearly Tax Base as an annual tax.',
    )

    @api.depends('yearly_tax_base')
    def _compute_employee_yearly_tax(self):
        for employee in self:
            yearly_tax_base = employee.yearly_tax_base
            if yearly_tax_base <= 40000:
                employee.employee_yearly_tax = 0
            elif yearly_tax_base <= 55000:
                employee.employee_yearly_tax = (yearly_tax_base * 0.1) - 4000
            elif yearly_tax_base <= 70000:
                employee.employee_yearly_tax = (yearly_tax_base * 0.15) - 6750
            elif yearly_tax_base <= 200000:
                employee.employee_yearly_tax = (yearly_tax_base * 0.20) - 10250
            elif yearly_tax_base <= 400000:
                employee.employee_yearly_tax = (yearly_tax_base * 0.225) - 15250
            elif yearly_tax_base <= 600000:
                employee.employee_yearly_tax = (yearly_tax_base * 0.25) - 25250
            elif yearly_tax_base <= 700000:
                employee.employee_yearly_tax = (yearly_tax_base * 0.25) - 21250
            elif yearly_tax_base <= 800000:
                employee.employee_yearly_tax = (yearly_tax_base * 0.25) - 18500
            elif yearly_tax_base <= 900000:
                employee.employee_yearly_tax = (yearly_tax_base * 0.25) - 15000
            elif yearly_tax_base <= 1200000:
                employee.employee_yearly_tax = (yearly_tax_base * 0.25) - 10000
            else:
                employee.employee_yearly_tax = (yearly_tax_base * 0.275) - 30000

    employee_monthly_tax = fields.Float(
        string="Employee Monthly Tax", 
        compute='_compute_employee_monthly_tax',
        help='The value of this field is calculated from dividing the Employee Yearly Tax by 12.',
    )

    @api.depends('employee_yearly_tax')
    def _compute_employee_monthly_tax(self):
        for employee in self:
            employee.employee_monthly_tax = employee.employee_yearly_tax / 12