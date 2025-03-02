from odoo import http
from odoo.http import request

class ResLanguages(http.Controller):

    @http.route('/owl/rpc/example', type="json", auth="none", csrf=False)
    def res_languages(self,**kwargs):
            languages=request.env['res.lang'].search_read([])
            return languages