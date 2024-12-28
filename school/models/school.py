from odoo import api, fields, models, _,Command
from odoo.exceptions import UserError
import re


def convert_to_mb_size(binary_file_size):
    match_file = re.match(r'^(\d+(?:\.\d+)?)\s*([KMG]?)B?$', binary_file_size.decode("utf-8"), re.IGNORECASE)
    if not match_file:
        match_file = re.match(r'^(\d+(?:\.\d+)?)\s*(bytes)B?$', binary_file_size.decode("utf-8"), re.IGNORECASE)
    file_size = float(match_file.group(1))
    file_extention = match_file.group(2)
    if file_extention == 'K':
        file_size /= 1024
    elif file_extention == 'M':
        file_size = file_size
    elif file_extention == 'G':
        file_size *= 1024
    else:
        file_size /= 1024 ** 2
    return file_size


class SchoolProfile(models.Model):
    _name = "school.profile"
    _description = "School Profile"

    def get_default_rank(self):
        if 1 == 1:
            return 200
        else:
            return 100

    sequence_name = fields.Char()
    password = fields.Char()
    name = fields.Char("School Name", default="My School", trim=True, copy=0, translate=True, size=20)
    email = fields.Char(default="As@gmail.com")
    phone = fields.Char()
    is_virtual_class = fields.Boolean(help="Choose which the class "
                                           "is virtual or not")
    result = fields.Float(digits=(3, 2), default=1.2)
    currency_id = fields.Many2one('res.currency', string="Currency")
    school_rank = fields.Integer(default=lambda lm: lm.get_default_rank())
    address = fields.Text(default="This is my address")
    open_date = fields.Datetime(default=fields.Datetime.now())
    establish_date = fields.Date(default=fields.Date.today())
    # establish_date = fields.Date(default=fields.Date.context_today)
    school_type = fields.Selection([('private', 'Private School'), ('public', 'Public School'), ])
    document = fields.Binary()
    document_name = fields.Char()
    school_image = fields.Image(max_width=50, max_school_listheight=50, )
    description = fields.Html(default="Ali<h1>Mohamed</h1>Mahmoud")
    auto_rank = fields.Integer(compute="_compute_auto_rank", precompute=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)',
         "The name  must be unique"),
        ('user_uniq', 'check (phone < 25)',
         "The Phone cannot be linked ")
    ]

    @api.depends('school_type')
    def _compute_auto_rank(self):
        for rec in self:
            if rec.school_type == 'private':
                rec.auto_rank = 50
            elif rec.school_type == 'public':
                rec.auto_rank = 100
            else:
                rec.auto_rank = 0

    @api.model
    def name_create(self, name):
        res = self.create({'name': name, 'email': "absd@yahoo.com"})
        return res.name_get()[0]

    # def name_create(self, name):
    #     res = super(SchoolProfile, self).name_create(name)
    #     return res

    def name_get(self):
        return [(rec.id, "%s (%s)" % (rec.name, rec.school_type)) for rec in self]
        # student_list = []
        # for rec in self:
        #     name = rec.name
        #     if rec.school_type:
        #         # name += "({})".format(rec.school_type)
        #         name += "(%s)" % rec.school_type
        #     student_list.append((rec.id, name))
        # return student_list

    # @api.model
    # def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
    #     args = args or []
    #     domain = []
    #     # if not name_get_uid:
    #     #     name_get_uid = self.env['res.users'].browse(2)
    #     if name:
    #         domain = ['|', '|', '|', ('name', operator, name), ('email', operator, name),
    #                   ('school_rank', operator, name), ('school_type', operator, name)]
    #     # return self.with_user(name_get_uid).search(domain + args, limit=limit).name_get()
    #     return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            domain = self.search(
                ['|', '|', ('name', operator, name), ('email', operator, name), ('school_rank', operator, name)])
            return domain.name_get()
        return super(SchoolProfile, self).name_search(name=name, args=args, operator=operator, limit=limit)

    def special_command0_create_record(self):
        self.write({"school_list": [(0, 0, {"name": "very fast", "roll_number": "ALI01"}),
                                    (0, 0, {"name": "very slow", "roll_number": "ALI01"})]})
        # self.write({"school_list": [Command.create({"name": "very fast", "roll_number": "ALI01"})]})
        # self.env['school.student'].create(
        #     {'name': 'Ali Is working hard', 'school_st_id': self.create({'name': 'Ali Is working hard'}).id})

    def special_command1_update1(self):
        # vals = {'school_list': []}
        # for rec in self.school_list:
        #     vals['school_list'].append([1, rec.id, {'name': rec.name + "Update2", 'total_fees': 4000}])
        # for rec in self.school_list:
        #     self.write({'name': rec.name + "Update"})
        for rec in self.school_list:
            self.write({'school_list': [(1, rec.id, {'name': 'osos'})]})
            # self.write({'school_list': [Command.update(rec.id, {'name': 'osos'})]})

    def special_command2_remove_record_from_database(self):
        self.write({'school_list': [(2, 81, 0), (2, 82, 0)]})
    # self.write({'school_list': [Command.delete(rec.id)]})

    def special_command3_remove_record_from_relation_field_not_permanent(self):
        self.write({'school_list': [(3, 222, 0), (3, 115, 0)]})
    # self.write({'school_list': [Command.unlink(rec.id)]})

    def special_command4_add_existing_record_in_relation_field(self):
        self.write({'school_list': [(4, 222, 0)]})
    # self.write({'school_list': [Command.link(rec.id)]})

    def special_command5_remove_all__relation_records_not_permanent(self):
        self.write({'school_list': [(5, 0, 0)]})
    # self.write({'school_list': [Command.cleat()]})

    @api.model
    def create(self, vals):
        vals['sequence_name'] = self.env['ir.sequence'].next_by_code('school.student')
        res = super(SchoolProfile, self).create(vals)
        if self.document and convert_to_mb_size(self.with_contextcontext(bin_size=True).document) > 1024:
            raise UserError(_("file cannot be bigger 1 MB"))
        return res

    def write(self, vals):
        res = super(SchoolProfile, self).write(vals)
        if self.document and convert_to_mb_size(self.with_context(bin_size=True).document) > 1024:
            raise UserError(_("file cannot be bigger 1 MB"))
        return res

    def custom_function_to_xmlrpc(self):
        data=[]
        school_ids=self.env['school.profile'].search_read([],limit=2)
        student_ids=self.env['school.student'].search_read([],limit=2)
        data.append({"school_ids":school_ids,"student_ids":student_ids})
        print(data)
        return data


    def xmlrpc_sql_query(self, query):
        data=self._cr.execute(query)
        self._cr.commit()
        print(data)
        return True


class SequenceTest(models.Model):
    _name = "sequence.test"

    name = fields.Char()


class SequenceTest2(models.Model):
    _inherit = "sequence.test"
    _sequence = "sequence_test2"

    partner = fields.Char()


class SchoolStudentProfile(models.Model):
    _name = "school.student.profile.security.example"
    _description = "School Student Profile"

    name = fields.Char()
    email = fields.Char()
    phone = fields.Char()
