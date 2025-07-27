from odoo import api, fields, models, _
from odoo import osv
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from datetime import timedelta


class PurchaseOrder(models.Model):
    _inherit =  "purchase.order"

    total_qty = fields.Float(store=True, compute="_total_qty")

    @api.depends('order_line.product_qty')
    def _total_qty(self):
        qty = 0
        for order in self:
            for line in order.order_line:
                qty += line.product_qty
            order.total_qty = qty
