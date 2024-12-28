from odoo import models, fields, api


class HREmployee(models.Model):

    _inherit = 'hr.employee'
    _description = "Generate employee sequence id"

    emp_id = fields.Char("Employee Id")

    @api.model
    def create(self, values):
        values['emp_id'] = self.env[
            'ir.sequence'].next_by_code('seqemp.seqemp')
        return super(HREmployee, self).create(values)

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