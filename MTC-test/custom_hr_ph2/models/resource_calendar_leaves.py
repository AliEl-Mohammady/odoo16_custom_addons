from odoo import fields, models

class ResourceCalendarLeaves(models.Model):
    _inherit = 'resource.calendar.leaves'

    is_public_holiday = fields.Boolean(string='Is Public Holiday', default=False)