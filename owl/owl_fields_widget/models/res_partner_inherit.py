from odoo import api, fields, models


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    user_name = fields.Char()
    salary = fields.Integer(string='Salary')
