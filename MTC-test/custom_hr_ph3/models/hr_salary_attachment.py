from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class HrSalaryAttachment(models.Model):
    _inherit = 'hr.salary.attachment'

    duration = fields.Selection([
        ('1_month', '1 Month'),
        ('3_months', '3 Months'),
        ('6_months', '6 Months'),
        ('1_year', '1 Year'),
    ], string='Duration', required=True, store=True, tracking=True, copy=True)

    @api.onchange('duration', 'total_amount')
    def _onchange_duration(self):
        if self.duration and self.total_amount:
            if self.duration == '1_month':
                self.monthly_amount = self.total_amount / 1
            elif self.duration == '3_months':
                self.monthly_amount = self.total_amount / 3
            elif self.duration == '6_months':
                self.monthly_amount = self.total_amount / 6
            elif self.duration == '1_year':
                self.monthly_amount = self.total_amount / 12

    @api.onchange('monthly_amount', 'duration')
    def _onchange_monthly_amount(self):
        if self.monthly_amount and self.duration:
            if self.duration == '1_month':
                self.total_amount = self.monthly_amount * 1
            elif self.duration == '3_months':
                self.total_amount = self.monthly_amount * 3
            elif self.duration == '6_months':
                self.total_amount = self.monthly_amount * 6
            elif self.duration == '1_year':
                self.total_amount = self.monthly_amount * 12

    # @api.constrains('total_amount', 'deduction_type')
    # def _check_total_amount(self):
    #     for attachment in self:
    #         if attachment.deduction_type == 'loans':
    #             if attachment.total_amount > 0.9 * attachment.employee_id.contract_id.wage:
    #                 raise ValidationError(_("Total amount cannot exceed 90% of employee's basic salary."))

    # def write(self, vals):
    #     if 'total_amount' in vals:
    #         for attachment in self:
    #             if 'employee_id' in vals:
    #                 employee_id = vals['employee_id']
    #             else:
    #                 employee_id = attachment.employee_id.id
    #             employee = self.env['hr.employee'].browse(employee_id)
    #             if attachment.deduction_type == 'loans' and vals['total_amount'] > 0.9 * employee.contract_id.wage:
    #                 raise ValidationError(_("Total amount cannot exceed 90% of employee's basic salary."))
    #     return super(HrSalaryAttachment, self).write(vals)