from odoo import api, Command, fields, models, _

class AccountMove(models.Model):
    _inherit = "account.move"