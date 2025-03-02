from odoo import http
from odoo.http import request

class ResPartner(http.Controller):

    @http.route('/owl/rpc', type="json", auth="none", csrf=False)
    def read_res_partners(self,limit):
            return request.env['res.partner'].sudo().search_read([],["name","email"],limit=limit)
