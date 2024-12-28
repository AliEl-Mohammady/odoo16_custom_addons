from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import random
from odoo import tools


class SchoolStudent(models.Model):
    _inherit = 'school.student'

    student_full_name = fields.Char()
