#from email.policy import default
from asyncore import file_dispatcher
from email.policy import default
from importlib.metadata import files
from typing_extensions import Required
from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError


class estate_property(models.Model):
    _name='estate.property'
    _description = 'estate properties model'
    _order = 'id desc'

    def _get_description(self):
        if self.env.context.get('is_my_property'):
            return self.env.user.name + "'s Property"

    name = fields.Char(required=True, string='Title', default="Unknown")
    description = fields.Text(default=_get_description)
    postcode = fields.Char()
    date_availablilty = fields.Date(string='Available From', default=fields.Date.today(), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, compute='_compute_sold')
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area =fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection([('new', 'New'), ('sold', 'Sold'), ('cancel', 'Cancel')], default="new")
    active = fields.Boolean(default=True)

    buyer = fields.Many2one('res.partner',copy=False)
    sales_person = fields.Many2one('res.users',default=lambda self: self.env.user)
    property_type_id = fields.Many2one('estate.property.type')

    tags_ids = fields.Many2many('estate.property.tags')

    offers_ids = fields.One2many('estate.property.offers','property_id')

    total_area = fields.Float(compute='_compute_total_area')

    best_price = fields.Float(compute="_compute_max_price") #compute="_compute_max_price" to run simple function.

    status = fields.Char(copy=False, default='New')

    
    
    def action_sold(self):
        for record in self:
            if record.status =='cancel':
                raise UserError("Cancel property cannot be sold")
            record.status='sold'
            record.state = 'sold'
    
    def action_cancel(self):
        for record in self:
            if record.status =='sold':
                raise UserError("Sold property cannot be cancel")
            record.status ='cancel'
            record.state = 'cancel'

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for area in self:
            area.total_area = area.living_area + area.garden_area
                           
    #used simple function for best_price
    @api.depends('offers_ids.price')
    def _compute_max_price(self):
        for record in self:
            max_price = 0
            for offer in record.offers_ids:
                if offer.price > max_price:
                    max_price = offer.price
            record.best_price = max_price
    
    #using mapped function for best_price
    @api.depends('offers_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offers_ids.mapped('price'))

    @api.onchange('garden')
    def _onchange_garden(self):
            if self.garden == True:
                self.garden_area = 10
                self.garden_orientation = 'north'
            else:
                self.garden_area = 0
                self.garden_orientation = None

    @api.depends('offers_ids.status')  
    def _compute_sold(self):
        for record in self:
            sold_price = 0
            buyer_name = None
            for offer in record.offers_ids:
                    if offer.status == 'accepted':
                        sold_price = offer.price
                        buyer_name = offer.partner_id
                        record.state = 'sold'
                        record.status = 'sold'
            record.selling_price = sold_price
            record.buyer = buyer_name

  #  @api.depends('offers_ids.status')  
  #  def _compute_sold(self):
  #      for record in self:
  #          sold_price = 0
  #          buyer_name = None
  #          for offer in record.offers_ids:
  #                  if offer.status == 'accepted':
  #                      if record.expected_price * (0.9)  >= offer.price:
  #                         raise ValidationError(_('The selling price must be greter or equal to 90 percent of expected price.'))
  #                      else:
  #                          sold_price = offer.price
  #                          buyer_name = offer.partner_id 
  #          record.selling_price = sold_price
  #          record.buyer = buyer_name     
 
    @api.constrains('offers_ids.price', 'expected_price')
    def _check_price(self):
        if self.offers_ids.status == 'accepted':
            if self.expected_price * (0.9) >= self.offers_ids.price:
                    raise ValidationError(_('The selling price must be greter or equal to 90 percent of expected price.'))


    _sql_constraints = [
                        ('check_expected_price', 'check(expected_price > 0.0)', 'The Expected price must be positive.'),
                        
    ]
                        
    def state_update(self):
        self.state = "received"
        return True


    def open_offer(self):
        return {
            "type" : "ir.actions.act_window",
            "res_model" : "estate.property.offers",
            "views":[[False,'tree']],
            "target":"new",
            "domain":['&',('status','=','accepted'),('property_id','=',self.id)]
        }

class estate_property_type(models.Model):
    _name='estate.property.type'
    _description = 'estate properties type model'
    _order = 'name'

    name = fields.Char(required=True, string='Title')
    property_ids = fields.One2many('estate.property','property_type_id')

    _sql_constraints = [('Unique_property_type_name', 'UNIQUE (name)', 'The Property Type name must be UNIQUE.')]


class estate_property_tags(models.Model):
    _name='estate.property.tags'
    _description = 'estate properties tags model'
    _order = 'name' 

    name = fields.Char(required=True, string='Title', editable=True)
    color = fields.Integer()
    _sql_constraints = [('Unique_property_tag_name', 'UNIQUE (name)', 'The Property Tag name must be UNIQUE.')]


class estate_property_offers(models.Model):
    _name='estate.property.offers'
    _description = 'estate properties offers model'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection([('accepted','Accepted'),('refused','Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    #property_type_id = fields.Many2one(related='property_id.property_type_id',store=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date', inverse="_inverse_date")
    
    _sql_constraints = [('check_price', 'check(price > 0.0)', 'Offer Price must be positive')]

    def action_accept(self):
        for record in self:
            record.status = 'accepted'
        return True
    
    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True

    @api.depends('validity')
    def _compute_date(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_date(self):
        for record in self:
            if record.create_date:
                if record.date_deadline:
                    record.validity = int((record.date_deadline - (record.create_date).date()).days)

    
class estate_myproperty(models.Model):
    _name = 'estate.myproperty'
    _description = 'estate myproperty model'

    name = fields.Char()

class ResPartner(models.Model):
    _inherit = "res.partner"

    is_buyer = fields.Boolean()

