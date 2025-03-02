# -*- coding: utf-8 -*-
from odoo import api, fields, models


class OwlTodoApp(models.Model):
    _name = 'owl.todo.list.app'
    _description = 'OWL Todo List App'

    name = fields.Char(string="Task Name")
    isCompleted = fields.Boolean()
    time = fields.Datetime()
