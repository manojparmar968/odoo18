# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo import osv
from odoo.exceptions import UserError


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = "name"

    name = fields.Char('Name', required=True, translate=True)
    color = fields.Integer('Color')

    _sql_constraints = [
        ('tag_name_unique', 'UNIQUE(name)', 'Property tag must be unique!'),
    ]