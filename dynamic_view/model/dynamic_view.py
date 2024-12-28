from odoo import models, fields, api, _, tools


class StudentSchoolDynamicView(models.Model):
    _name = 'student.school.dynamic.view'
    _description = 'student school dynamic view'
    _auto = False #prevent create a table

    school_name = fields.Char()
    school_phone = fields.Char()
    school_email = fields.Char()
    school_type = fields.Selection([('private', 'Private School'), ('public', 'Public School'), ])
    student_name = fields.Char()
    student_rno = fields.Char()
    student_fees = fields.Float()
    student_seq = fields.Integer()


    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            create or replace view {} as (
                    select std.id as id,
                     std.roll_number as student_rno,
                     std.name as student_name,
                     std.student_fees as student_fees,
                     std.student_seq as student_seq,
                     sp.name as school_name,
                     sp.phone as school_phone,
                     sp.email as school_email,
                     sp.school_type as school_type
                    from school_student as std join school_profile as sp on std.school_st_id=sp.id)"""
                            .format(self._table))
