import json

from odoo import http
from odoo.http import request
from base64 import b64encode


class FilePondController(http.Controller):

    @http.route('/file/process',type='http', auth='user', methods=["POST"],csrf=False)
    def filePond_process(self):
        filepond=request.params.get("filepond")
        file=b64encode(filepond.read())
        attachment=request.env["ir.attachment"].create({
            "name":filepond.filename,
            "datas":file
        })
        print(attachment)
        if attachment :
            return str(attachment.id)
        else:
            return ""


    @http.route('/file/revert',type='http', auth='user', methods=["DELETE"],csrf=False)
    def filePond_revert(self):
        id=json.loads(request.httprequest.data)
        print(id)
        attachment=request.env["ir.attachment"].search([("id","=",id)])
        if attachment:
            attachment.unlink()
        else:
            return ""
        print("Hello from inside endpoint",request.httprequest)
        print("Hello from inside endpoint",attachment)

