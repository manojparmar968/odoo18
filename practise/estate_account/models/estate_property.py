from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_property_sold(self):
        res = super(EstateProperty, self).action_property_sold()
        Move = self.env['account.move']
        for property in self:
            commission_amount = property.selling_price * 0.06
            admin_fee = 100.00
            move_vals = {
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',  # Customer Invoice
                'line_ids': [],
                'invoice_line_ids': [(0,0, {
                    'name': property.name,
                    'quantity': 1,
                    'price_unit': property.selling_price,
                }),
                (0,0, {
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': admin_fee,
                })
                ]
            }
            move = Move.create(move_vals)
        return res