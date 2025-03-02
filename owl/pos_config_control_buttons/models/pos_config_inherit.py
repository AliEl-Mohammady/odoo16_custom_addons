from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import random
from odoo import tools


class PosConfigInherit(models.Model):
    _inherit = 'pos.config'

    visible_discount_control = fields.Boolean()



class PosSessionInherit(models.Model):
    _inherit = 'pos.session'

    def _pos_data_process(self, loaded_data):
        super()._pos_data_process(loaded_data)
        loaded_data["visible_discount_control"]=self.config_id.visible_discount_control
