from odoo import models, fields, api, SUPERUSER_ID
from odoo.http import Request


def _first_pre_init_hook(cr):
    print("Pre init hook before install module")
    cr.execute("""update res_partner set mobile='0102568798' where mobile is null""")
    cr.commit()

    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.partner'].hook_method()


def _second_post_init_hook(cr, registry):
    print("Post init hook after install module")
    cr.execute("""update res_partner set vat='12345' where vat is null""")
    cr.commit()

    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.partner'].write({'mobile': '112233'})

def _thierd_uninstall_hook(cr, registry):
    print("uninstall hook after uninstall module")
    cr.execute("""update res_partner set vat=' ' where vat='12345'""")
    cr.commit()

    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.partner'].hook_method()


def _post_load_hook():
    print("Good")
#     patch_set_handler=WebRequest.set_handler
#
#     def set_handler()
