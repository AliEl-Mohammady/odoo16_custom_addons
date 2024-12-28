from odoo import fields, models, api

class HrContractHistory(models.Model):
    _inherit = 'hr.contract.history'

    date_join= fields.Date(
        string= "Join Date",
        required = True,
        related='employee_id.date_join',
    )

    emp_id = fields.Char("Employee Id", related='employee_id.emp_id', readonly=True)