from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, AccessError
from datetime import timedelta
from dateutil.relativedelta import relativedelta

direction = [
    ('north', 'North'), 
    ('south', 'South'),
    ('east', 'East'), 
    ('west', 'West')
]

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text('Description')
    postcode = fields.Char('PostCode')
    date_availability = fields.Date('Available From',copy=False, default=lambda self: fields.Datetime.today() + relativedelta(days=90))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price',readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms',default = 2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(direction, string='Garden Orientation', default='north')
    qr = fields.Binary(string="QR Code")
    active = fields.Boolean(default=True, help="Set active to false to hide the record without removing it.")
    state = fields.Selection(string='Status', selection=[
        ('new', 'New'), ('offer_received', 'Offer Received'),('offer_accepted', 'Offer Accepted'), 
        ('sold', 'Sold'), ('canceled', 'Canceled')
        ], copy=False, required=True, default='new',
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesman_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offer')
    total_area = fields.Integer("Total Area (sqm)", compute="_compute_total_area", store=True)
    best_price = fields.Float("Best Price", compute="_compute_best_price", store=True)

    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price > 0)', 'Expected Price should be positive.'),
        ('positive_selling_price', 'CHECK(selling_price > 0)', 'Selling Price should be positive.'),
    ]

    @api.onchange('garden')
    def on_change_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = ''
            self.garden_orientation = ''

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for area in self:
            area.total_area = (area.living_area + area.garden_area)

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for offer in self:
            offer.best_price = max(offer.offer_ids.mapped('price')) if offer.offer_ids else 0

    def action_property_sold(self):
        self.ensure_one()
        if self.state == 'canceled':
            raise UserError(_('A cancelled property cannot be sold'))
        else:
            self.state = 'sold'
    
    def action_property_cancel(self):
        self.ensure_one()
        if self.state == 'sold':
            raise UserError(_('A sold property cannot be cancelled'))
        else:
            self.state = 'canceled'

    # def unlink(self):
    # return super(EstateProperty, self).unlink()
    @api.ondelete(at_uninstall=False)
    def _check_can_be_deleted(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError(_("You cannot delete this property unless its state is %s'.",record.state))
        