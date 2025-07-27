# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo import osv
from odoo.exceptions import UserError


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = "name"

    sequence = fields.Integer("Sequence", default=1)
    name = fields.Char('Name', required=True, translate=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(string='Offer Count', compute="_compute_offer_count", store=True)

    _sql_constraints = [
        ('type_name_unique', 'UNIQUE(name)', 'Property type must be unique!'),
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)
            # Alternative
            # rec.offer_count = len(rec.property_ids.offer_ids)