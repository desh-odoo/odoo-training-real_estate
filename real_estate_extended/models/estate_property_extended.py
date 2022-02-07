from sys import setdlopenflags
from attr import field
from odoo import api, fields, models, _


class estate_property_extended(models.Model):
    _inherit = "estate.property"

    property_ids = fields.One2many('estate.property', 'sales_person')
    new_field = fields.Char()


class estate_property_lease(models.Model):
    _name = 'estate.property.lease'
    _inherits = {'estate.property': 'estate_property_id'}

    estate_property_id = fields.Many2one('estate.property')

    lease_duration = fields.Integer(string="Lease Duration(Years)")
    price_yearly = fields.Float(compute="_compute_price_yearly")

    @api.depends('lease_duration', 'expected_price')
    def _compute_price_yearly(self):
        for record in self:
            record.price_yearly = 12 * record.expected_price


class ResPartner(models.Model):
    _inherit = "res.users"
    property_id = fields.One2many('estate.property', 'sales_person')
