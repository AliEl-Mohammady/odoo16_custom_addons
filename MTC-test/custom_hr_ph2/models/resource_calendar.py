from odoo import api, fields, models, _
from operator import itemgetter
from odoo.addons.resource.models.resource import Intervals
from pytz import timezone
from datetime import datetime, time, timedelta
from dateutil import rrule

class ResourceCalendarAttendance(models.Model):
    _inherit = 'resource.calendar.attendance'

    shift_hours = fields.Float(string='Shift Hours', compute='_compute_shift_hours', store=True)
    is_cross_shift = fields.Boolean(string='Is Cross Shift')
    overtime_after = fields.Float(string='Overtime After', store=True)

    hour_from = fields.Float(string='From Hour')
    hour_to = fields.Float(string='To Hour')

    @api.depends('hour_from', 'hour_to', 'is_cross_shift', 'overtime_after')
    def _compute_shift_hours(self):
        for shifts in self:
            if shifts.hour_from and shifts.hour_to:
                if shifts.is_cross_shift:
                    shifts.shift_hours = shifts.hour_to - shifts.hour_from + shifts.overtime_after
                else:
                    shifts.shift_hours = shifts.hour_to - shifts.hour_from
            else:
                shifts.shift_hours = 0.0