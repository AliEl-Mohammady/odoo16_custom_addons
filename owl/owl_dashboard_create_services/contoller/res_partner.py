from odoo import http
from odoo.http import request

class ResPartnerCount(http.Controller):

    @http.route('/owl/dashboard/rpc', type="json", auth="none", csrf=False)
    def count_res_partners(self):
            partner=request.env['res.partner'].sudo()
            return {
                "partners": partner.search_count([]),
                "customers": partner.search_count([('is_company', '=', True)]),
                "individuals": partner.search_count([('is_company', '=', False)]),
                "locations": len(partner.read_group([], ['state_id'], ['state_id'])),
            }