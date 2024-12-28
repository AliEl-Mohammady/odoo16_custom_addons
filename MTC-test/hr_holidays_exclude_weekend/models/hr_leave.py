# Copyright 20120 Shabeer VPK
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.exceptions import UserError

import pytz

from collections import namedtuple, defaultdict

from pytz import timezone, UTC

from odoo import api, fields, models, tools
from odoo.addons.base.models.res_partner import _tz_get
from odoo.addons.resource.models.resource import float_to_time, HOURS_PER_DAY
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import format_date
from odoo.tools.translate import _
from odoo.osv import expression


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    # @api.onchange('holiday_status_id')
    # def recompute_no_days(self):
    #     self._onchange_leave_dates()

    # def _get_number_of_days(self, date_from, date_to, employee_id):
    #     context_data = {'employee_id' : employee_id,
    #                     'from_leave_request': True,
    #                     'exclude_weekends' : False}
    #
    #     if (self.holiday_status_id.exclude_weekends or
    #             not self.holiday_status_id):
    #         context_data['exclude_weekends'] = True
    #
    #     instance = self.with_context(context_data)
    #     return super(HrLeave, instance)._get_number_of_days(
    #         date_from,
    #         date_to,
    #         employee_id,
    #     )

    def diff_dates(self, date_from, date_to):
        return abs(date_to - date_from).days

    # def _get_number_of_days_batch(self, date_from, date_to, employee_ids):
    #     """ Returns a float equals to the timedelta between two dates given as string."""
    #     employee = self.env['hr.employee'].browse(employee_ids)
    #     # We force the company in the domain as we are more than likely in a compute_sudo
    #     domain = [('time_type', '=', 'leave'),
    #               ('company_id', 'in', self.env.company.ids + self.env.context.get('allowed_company_ids', []))]
    #
    #     result = employee._get_work_days_data_batch(date_from, date_to, domain=domain)
    #     for employee_id in result:
    #         if self.request_unit_half and result[employee_id]['hours'] > 0:
    #             result[employee_id]['days'] = 0.5
    #     return result

    def _get_number_of_days_batch(self, date_from, date_to, employee_ids):
        """ Returns a float equals to the timedelta between two dates given as string."""
        employee = self.env['hr.employee'].browse(employee_ids)
        # We force the company in the domain as we are more than likely in a compute_sudo
        domain = [('company_id', 'in', self.env.company.ids + self.env.context.get('allowed_company_ids', []))]

        result = employee._get_work_days_data_batch(date_from, date_to, domain=domain)
        if self.holiday_status_id.include_weekends:
            for key, value in result.items():
                if value['days'] == 0:
                    raise UserError("Days That You choose is already a weekend")
                hours_per_day = value['hours'] / value['days']
                days = self.diff_dates(date_from, date_to) if self.diff_dates(date_from,
                                                                              date_to) == 1 else self.diff_dates(
                    date_from, date_to) + 1
                value['days'] = days
                value['hours'] = value['days'] * hours_per_day

            for employee_id in result:
                if self.request_unit_half and result[employee_id]['hours'] > 0:
                    result[employee_id]['days'] = 0.5

        else:
            result = super(HrLeave, self)._get_number_of_days_batch(date_from, date_to, employee_ids)

        return result

    def _get_number_of_days(self, date_from, date_to, employee_id):
        """ Returns a float equals to the timedelta between two dates given as string."""

        if self.holiday_status_id.include_weekends:
            days = self.diff_dates(date_from, date_to) if self.diff_dates(date_from,
                                                                          date_to) == 1 else self.diff_dates(
                date_from, date_to) + 1
            days = days
            hours = days * HOURS_PER_DAY
            result = {'days': days, 'hours': hours}
        else:
            result = super(HrLeave, self)._get_number_of_days(date_from, date_to, employee_id)

        return result
