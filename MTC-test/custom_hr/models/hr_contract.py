from odoo import fields, models, api
from odoo.exceptions import ValidationError

class HrContract(models.Model):
    _inherit = 'hr.contract'

    resource_calendar_id = fields.Many2one('resource.calendar', string='Working Hours', compute='_compute_resource_calendar_id', store=True)

    @api.depends('employee_id.resource_calendar_id')
    def _compute_resource_calendar_id(self):
        for contract in self:
            contract.resource_calendar_id = contract.employee_id.resource_calendar_id

    date_join= fields.Date(
        string= "Join Date",
        required = True,
        tracking=True,
        related='employee_id.date_join',
    )

    contract_type = fields.Selection([
        ('limited', 'Limited'),
        ('unlimited', 'Unlimited')
    ], string='Contract Type', store=True, tracking=True)

    contract_type_id = fields.Many2one(string='Employment Type')

    emp_id = fields.Char("Employee Id", related='employee_id.emp_id', readonly=True)

    @api.constrains('contract_type', 'date_start', 'date_end', 'contract_type_id')
    def _check_contract_type(self):
        for record in self:
            if record.contract_type == "limited" and not record.contract_type_id:
                raise ValidationError("When the contract type is Limited, employment Type must be set.")
            
            if record.contract_type == "limited" and (not record.date_start or not record.date_end):
                raise ValidationError("When the contract type is Limited, both start date and end date must be set.")
            

            if record.contract_type != "limited" and record.contract_type_id and record.date_start and record.date_end:
                pass