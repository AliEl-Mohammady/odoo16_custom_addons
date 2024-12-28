from odoo import fields, models, api

class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    holiday_days = fields.Integer(string='Holiday Days', store=True)

    minimum_months_required = fields.Integer(
        string="Minimum Months Required",
        help="The minimum number of months required for the leave eligibility."
    )

    max_days_per_month = fields.Integer(
        string="Maximum Days Allowed per Month",
        help="The maximum number of days allowed for the time off per month."
    )