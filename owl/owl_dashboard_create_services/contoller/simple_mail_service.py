from odoo import http
from odoo.http import request

class ResPartnerCount(http.Controller):

    @http.route('/owl/dashboard/simple_mail_service', type="json", auth="none", csrf=False)
    def simple_mail_service(self,**data):
            email=request.env['mail.mail'].sudo()
            mail_date= {
                "email_from": data['email_from'],
                "email_to": data['email_to'],
                "subject": data['subject'],
                "body_html": data['message'],
            }
            email_send=email.create(mail_date).send()
            if email_send:
                print("true")
                return True
            else:
                print("false")
                return False