from odoo import _, api, fields, models
from odoo.tools import SQL


class Users(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'salesman_id', string='Properties',
        domain=[('state', 'in', ('new', 'offer_received', 'offer_accepted'))])