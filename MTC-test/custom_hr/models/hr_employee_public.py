from odoo import models, fields, api

class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    emp_id = fields.Char("Employee Id", related='employee_id.emp_id')    
    
    def name_get(self):
        result = []
        for rec in self:
            emp_id_str = str(rec.emp_id) if rec.emp_id else ''
            name = '[' + emp_id_str + ']' + ' ' + rec.name
            result.append((rec.id, name))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = ['|', ('emp_id', operator, name), ('name', operator, name)]
        records = self.search(domain + args, limit=limit)
        return records.name_get()