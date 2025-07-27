# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo import osv
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from datetime import timedelta, date


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = "price desc"

    price = fields.Float('Price')
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], string='Status', copy=False)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer("Validity (days)", default = 7)
    date_deadline = fields.Date("Deadline", compute="_compute_date_deadline", inverse='_inverse_date_deadline', store=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', string='Property Type', store=True)
    

    _sql_constraints = [
        ('positive_price', 'CHECK(price > 0)', 'Offer Price should be positive.'),
    ]

    @api.constrains('price')
    def _check_offer_price(self):
        if self.price < (self.property_id.expected_price * 0.90):
            raise ValidationError(_("A selling Price must be at least 90'%' of the expected price."))

    @api.depends('validity')
    def _compute_date_deadline(self):
        for day in self:
            print(day.validity)
            if day.create_date and day.validity:
                day.date_deadline = day.create_date + timedelta(days = day.validity)
            # Alternate
            # day.date_deadline = date.today() + timedelta(days = day.validity)

    def _inverse_date_deadline(self): # Inverse is not working
        for record in self:
            if record.date_deadline and record.create_date:
                # If date_deadline is set, calculate the validity
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days
            elif record.create_date: # elif record.validity and record.create_date:
                # If validity is set, calculate the date_deadline
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            # Alternate
            # record.validity = record.validity + (record.date_deadline-date.today()).days

    def action_accept_offer(self):
        self.ensure_one()
        self.status = 'accepted'
        self.property_id.write({
            'selling_price' : self.price,
            'buyer_id' : self.partner_id.id,
            'state': 'offer_accepted'
        })
        return True
        # Alternative
        # if self.status == False and self.status != 'refused':
        #     self.status = 'accepted'
        #     self.property_id.selling_price = self.price
        #     self.property_id.buyer_id = self.id
        #     self.property_id.state = 'offer_accepted'
        # elif self.status == 'accepted':
        #     raise UserError(_("You already accept the offer."))
        # else:
        #     raise UserError(_('You Refused the offer So, You can not accept it.'))

    def action_refuse_offer(self):
        self.ensure_one()
        self.status = 'refused'
        # Alternative
        # if self.status == False and self.status != 'accepted':
        #     self.status = 'refused'
        # elif self.status == 'refused':
        #     raise UserError(_('You Already Refused the Offer.'))
        # else:
        #     raise UserError(_('You Accept the offer So, You can not cancelled it.'))

    @api.model_create_multi
    def create(self, vals_list):
        exist_rec = self.env['estate.property'].browse(vals_list[0]['property_id'])
        if exist_rec.exists():
            if exist_rec.best_price > vals_list[0]['price']:
                raise UserError(_("The Offer Must be Higher than %s.",exist_rec.best_price))
            exist_rec.write({'state': 'offer_received'})
        return super().create(vals_list)