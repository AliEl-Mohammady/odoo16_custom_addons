from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

#Insurance:
    insurance_exempt_rate = fields.Float(string="Insurance Exempt Rate", required=False)
    employee_share_rate = fields.Float(string="Employee Share Rate", required=False)
    company_share_rate = fields.Float(string="Company Share Rate", required=False)
    emergency_fund_rate = fields.Float(string="Emergency Fund Rate", required=False)

#Taxes:
    yearly_personal_exempted = fields.Float(string="Yearly Personal Exempted", required=False)


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update({
            'insurance_exempt_rate': float(self.env['ir.config_parameter'].sudo().get_param('custom_hr.insurance_exempt_rate')),
            'employee_share_rate': float(self.env['ir.config_parameter'].sudo().get_param('custom_hr.employee_share_rate')),
            'company_share_rate': float(self.env['ir.config_parameter'].sudo().get_param('custom_hr.company_share_rate')),
            'emergency_fund_rate': float(self.env['ir.config_parameter'].sudo().get_param('custom_hr.emergency_fund_rate')),
            'yearly_personal_exempted': float(self.env['ir.config_parameter'].sudo().get_param('custom_hr.yearly_personal_exempted')),
        })
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('custom_hr.insurance_exempt_rate', str(self.insurance_exempt_rate))
        self.env['ir.config_parameter'].sudo().set_param('custom_hr.employee_share_rate', str(self.employee_share_rate))
        self.env['ir.config_parameter'].sudo().set_param('custom_hr.company_share_rate', str(self.company_share_rate))
        self.env['ir.config_parameter'].sudo().set_param('custom_hr.emergency_fund_rate', str(self.emergency_fund_rate))
        self.env['ir.config_parameter'].sudo().set_param('custom_hr.yearly_personal_exempted', str(self.yearly_personal_exempted))