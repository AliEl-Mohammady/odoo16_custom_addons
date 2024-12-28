from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import datetime
from datetime import date
from dateutil import relativedelta


class student_fees_update_wizard(models.TransientModel):
    _name = "student.fees.update.wizard"
    _description = "student fees update wizard"

    fees = fields.Float()
    students_ids = fields.Many2many('school.student')

    def update_fees(self):
        print("Hello Ali")
        # self.env['school.student'].browse(self._context.get("active_ids")).update({'total_fees': self.fees})
        self.students_ids.write({'total_fees': self.fees})
        return True

    @api.model
    def default_get(self,field):
        res=super(student_fees_update_wizard,self).default_get(field)
        res['students_ids']=self.env['school.student'].browse(self.env.context.get("active_ids"))
        return res


class student_fees_update_inherit_wizard(models.TransientModel):
    _inherit = "student.fees.update.wizard"

    partner_name = fields.Char(string='Partner_name', required=False)

    def update_fees(self):
        print("Hello Ali")
        # to call the basic method must use super
        res = super(student_fees_update_inherit_wizard, self).update_fees()
        return True

# () paranthess