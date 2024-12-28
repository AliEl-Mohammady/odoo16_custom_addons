from odoo import models, fields, api, _, registry, tools
from odoo.exceptions import ValidationError, UserError
import random
from lxml import etree


class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'school_student.school_student'
    _order = 'student_seq,id'
    _log_access = True
    _inherit = ['mail.thread', 'mail.activity.mixin']

    student_seq = fields.Integer()
    name = fields.Char()
    roll_number = fields.Char()
    address_id = fields.Many2one('res.partner')
    school_st_id = fields.Many2one("school.profile", string="School", default=1,
                                   domain="[('is_virtual_class','=',True)]"
                                   # domain="[('currency_id','=',currency_id)]"
                                   # domain="[('currency_id.name','=','EUR')]"
                                   )
    address = fields.Text(related="school_st_id.address", store=1)
    hobby_ids = fields.Many2many("hobby", "student_hobby_rel", "student_id", "hobby_id", string="Hoppy", )
    hobbies_ids = fields.Many2one("hobby", )
    student_fees = fields.Monetary()
    ref_id = fields.Reference(selection=[('account.move', 'Account'), ('school.profile', 'School')], string="Reference",
                              # default="school.profile,1"
                              )
    total_fees = fields.Float()
    currency_id = fields.Many2one('res.currency', string="Currency")
    user_id = fields.Many2one('res.users')
    active = fields.Boolean(default=1)
    birth_date = fields.Date(groups="school.student_mid_group")
    country_id = fields.Many2one('res.country', string="Country")
    student_image = fields.Image()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'Progress'),
        ('paid', 'Paid'),
        ('done', 'Done')], string='State', default='draft')

    def wizard_button(self):
        action = self.env["ir.actions.act_window"]._for_xml_id("school_student.student_fees_update_wizard_action")
        return action
        # return {
        #         'type': 'ir.actions.act_window',
        #         'res_model': 'student.fees.update.wizard',
        #         'view_mode': 'form',
        #         'target': 'new'
        #     }

    def return_string_inside_email_template(self):
        return "Ali Mohamed Mahmoud"

    @api.model
    def create(self, vals):
        res = super(SchoolStudent, self).create(vals)
        message = f"{self.name} ,Creation Successfully"
        self.env['bus.bus']._sendone(
            self.env.user.partner_id,
            # self.env['res.partner'].browse(2),
            'simple_notification', {
            'title': _('Warning'),
            'type': 'success',
            'message': 'S`uccessfully Create',
            'sticky': False, })
        # school_profile = [{'name': 'Ahmed', 'email': 'ahmed@yahoo.com'}, {'name': 'Ziad'}]
        # vals = self.env['school.profile'].create(school_profile)
        return res

    def write(self, values):
        values['active'] = True
        res = super(SchoolStudent, self).write(values)
        return res

    @api.returns('self', lambda value: value.id)
    def copy(self, default={}):
        default['name'] = "copy(" + self.name + ")"
        res = super(SchoolStudent, self).copy(default=default)
        # res.name = _("%s(copy)") % self.name
        return res

    def unlink(self):
        for rec in self:
            if rec.student_fees == 100:
                raise UserError(_("can not be deleted"))
        res = super(SchoolStudent, self).unlink()
        return res

    @api.model
    def default_get(self, fields):
        res = super(SchoolStudent, self).default_get(fields)
        res['name'] = 'New Name'
        res['student_fees'] = 1500
        return res

    # def exists_method(self):
    #     students = self.env['school.student'].browse([1, 2, 5, 8, 4, 15, 78, 12])
    #     for rec in students:
    #         try:
    #             print(rec.id, "=>", rec.name)
    #         except Exception as e:
    #             print("this id is not exists")
    #
    def exists_method(self):
        students = self.env['school.student'].browse([1, 2, 5, 8, 4, 15, 78, 12])
        for rec in students:
            if rec.exists():
                print(rec.id, "=>", rec.name)
            else:
                print("this id is not exists")

    def ensure_one_method(self):
        self.ensure_one()
        print(self.name)
        print(self.school_st_id.name)
        # equal to for rec in self

    def get_meta_data_method(self):
        print(self.get_metadata())
        # [{'id': 147, 'create_uid': (2, 'Mitchell Admin'), 'create_date': datetime.datetime(2024, 2, 11, 19, 29, 34, 309995),
        # 'write_uid': (1, 'OdooBot'), 'write_date': datetime.datetime(2024, 2, 11, 19, 34, 4, 519588), 'xmlid': False, 'noupdate': False, 'xmlids': []}]

    def fields_get_method(self):
        self.fields_get()
        print(self.fields_get(['name', 'student_fees']))
        print(self.fields_get(['name', 'student_fees'], ['type', 'required']))

    def read_group_method(self):
        students = self.env['school.student']
        print(students.read_group([], fields=['school_st_id'], groupby=['address_id']))
        # [{'address_id_count': 1, 'address_id': (26, < odoo.tools.func.lazy object at 0x7f95780a8940 >),
        #   '__domain': [('address_id', '=', 26)]},
        #  {'address_id_count': 1, 'address_id': (33, < odoo.tools.func.lazy object at 0x7f95780a20c0 >),
        #   '__domain': [('address_id', '=', 33)]},
        #  {'address_id_count': 114, 'address_id': False, '__domain': [('address_id', '=', False)]}]

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(SchoolStudent, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                         submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            name_field = doc.xpath("//field[@name='name']")
            if name_field:
                name_field[0].set("string", "New Name")
            res['arch'] = etree.tostring(doc, encoding='unicode')
            if name_field:
                name_field[0].addnext(etree.Element('label', {'string': 'Hoppy', 'name': 'hoppy'}))
            res['arch'] = etree.tostring(doc, encoding='unicode')
            if name_field:
                name_field[0].addprevious(etree.Element('field', attrib={
                    'name': 'number',
                    'string': 'Number field from python file to xml ',
                    'invisible': '0',
                    'type': 'int',
                }))
            res['arch'] = etree.tostring(doc, encoding='unicode')

        if view_type == 'tree':
            doc = etree.XML(res['arch'])
            name_field = doc.xpath("//field[@name='name']")
            if name_field:
                name_field[0].set("string", "New Name")
            res['arch'] = etree.tostring(doc, encoding='unicode')
            print("edxvd", res['arch'])
        return res

    def custom_button_method(self):
        print(self.env.is_superuser)
        print(self.env.user)
        print(self.env.uid)
        print(self.env.company)
        print(self.env.companies)
        print(self.env.context)

        cl = tools.config.options
        print(cl["db_port"])
        # if cl.get("db_user") == "'odoo16ee'":
        #     cl["db_user"] = "odoo16e"

        # SQL QUERY
        # (creating a table inside db)
        # create table table_name (id int, name text, salaryreal,fieeld type);
        # (create a constraint inside table)
        # alter table ali add constraint constrain_name check (condition(salary > 5));
        self.env.cr.execute("select * from school_student")
        self.env.cr.commit()
        self.env.cr.execute("select count(*) from school_student")
        self.env.cr.commit()
        self.env.cr.execute("update school_student set active=True where name='Ali mohamed mahmoud'")
        self.env.cr.commit()
        self.env.cr.execute("delete from school_student where id=5")
        self._cr.commit()
        self.env.cr.execute("insert into school_student(name) values('Ali m mahmoud')")
        self.env.cr.commit()

        self.custom_method(random.randint(1, 1000), 'Ali')

    def custom_method(self, attr1, ali):
        self.total_fees = attr1
        self.name = ali

    def env_orm_button(self):
        students_user = self.env['res.users'].browse(6)
        students_company = self.env['res.company'].browse(2)
        create = self.env['res.partner'].with_user(students_user).create({'name': 'with_user'})
        create = self.env['res.partner'].with_company(students_company).create({'name': 'with_company'})
        new_cr = registry(self.env.cr.dbname).cursor()
        partner_id = self.env['res.partner'].with_env(self.env(cr=new_cr)).create({'name': 'env_cr'})
        partner_id._cr.commit()
        return create

    @api.model
    def roll_number_change(self):
        for rec in self.search([('roll_number', '=', False)]):
            rec.roll_number = "STD0" + str(rec.id)

    @api.onchange("school_st_id")
    def _onchange_domain(self):
        first_id = 0
        if self.school_st_id:
            first_id = self.school_st_id.currency_id.name
        return {"domain": {"currency_id": [("name", "=", first_id)]}}

    def special_command6_replace_many2many_field_with_new_existing_records(self):
        self.write({'hobby_ids': [(6, 0, [2, 3, 4])]})

    def check_button(self):
        raise UserError(_("Clicked Successfully"))

    def share_facebook(self):
        return {
            'type': 'ir.actions.act_url',
            # 'url': self.url,
            # 'url': 'web',
            'url': 'http://facebook.com',
            'target': 'new',
        }

    def print_button(self):
        return self.env.ref("qweb_header_footer_pdf_examples.student_header_footer_report_ids").report_action(self)

    def action_send_email(self):
        return self.env.ref('email_template.student_template_emails').send_mail(self.id, force_send=True)

    def login_button(self):
        # self.message_post(body="Hello user.") #simple example
        # self.message_post(body="<h3>Hello user.</h2>")  #HTML example
        self.message_post(body="<a href='http://facebook.com'> Facebook</a>Go to Facebook")  # website example

    def header_open_wiz(self):
        return {
            'name': _('Open Wizard'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'student.fees.update.wizard',
            'target': 'new',
            'context': {'default_students_ids': self.env.context.get('active_ids')}
        }


class SchoolProfile(models.Model):
    _inherit = "school.profile"

    school_list = fields.One2many('school.student', "school_st_id", string="Student List")
    school_count = fields.Integer(compute="compute_school_count")

    @api.depends('school_list')
    def compute_school_count(self):
        for rec in self:
            rec.school_count = len(rec.school_list)

    def smart_button(self):
        return {
            'name': _("Students"),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'school.student',
            'domain': [('id', 'in', self.school_list.ids)]
        }

    # first method to do name_search method
    # @api.model
    # def name_search(self, name, args=None, operator='ilike', limit=100):
    #     args = args or []
    #     if name:
    #         domain = self.search(
    #             ['|', '|', ('name', operator, name), ('email', operator, name), ('school_rank', operator, name)])
    #         return domain.name_get()
    #     return super(SchoolProfile, self).name_search(name=name, args=args, operator=operator, limit=limit)
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', '|', ('name', operator, name), ('email', operator, name),
                      ('school_rank', operator, name)]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)


class Hobby(models.Model):
    _name = "hobby"

    name = fields.Char(string="Hobbies")
    school_student_id = fields.Many2one('school.student')
    active = fields.Boolean(default=1)


class student_test_fees(models.Model):
    _name = "student.test.fees"
    _table = "student_test_fees"

    name = fields.Char(string="Fees")


class Partner(models.Model):
    _inherit = "res.partner"

    @api.model
    def create(self, vals):
        print("env", self.env)
        print("env", self.env.user)
        print("env", self.env.company)
        print("env", self.env.companies)
        print("env", self.env.context)
        # custom_context = self.env.context
        # custom_context['default_mobile'] = '0125858988'
        context = dict(self._context)
        print(context)
        context.setdefault('default_email', 'AAAAA')
        print(context)
        return super(Partner, self.with_context(context)).create(vals)


class Car(models.Model):
    _name = "car"

    name = fields.Char(string="Car Name")
    price = fields.Float(string="Car Name")


class CarEngines(models.Model):
    _name = "car.engines"
    _inherits = {"car": "car_id"}
    # _inherits = {"key_model_name": "value_field_many2one"}

    name = fields.Char(string="CarEngines")
    car_id = fields.Many2one('car')


class ResPartner(models.Model):
    _inherit = "res.partner"

    def hook_method(self):
        for rec in self.search([]):
            print("HOOK METHOD", rec.display_name)


class Country(models.Model):
    _inherit = "res.country"

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        res = super(Country, self).name_search(name=name, args=args, operator=operator, limit=limit)
        ctx = self.env.context
        std_ctx = ctx.get("students")
        stds = []
        country_list = []
        for std in std_ctx:
            if std[0] == 4:
                std_id = self.env['school.student'].search([('id', '=', std[1]), ('country_id', '!=', False)])
                if std_id:
                    country_list.append(std_id.country_id.id)
            if std[0] == 0:
                country_id = std[2].get('country_id')
                if country_id:
                    country_list.append(country_id)
            if std[0] == 1:
                country_id = std[2].get('country_id')
                if country_id:
                    country_list.append(country_id)
        if country_list:
            new_res_list = []
            for country in res:
                if country[0] not in country_list:
                    new_res_list.append(country)
            return new_res_list
        return res
