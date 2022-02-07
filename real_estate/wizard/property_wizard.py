from attr import field
from odoo import api, fields, models, _

class property_wizard(models.TransientModel):
    _name = "property.wizard"
    _description = "wizard"
    
    price = fields.Char()
    partner_id = fields.Many2one('res.partner', 'Name')   

    def action_add_offer(self):
        self.ensure_one()
        activeIds = self.env.context.get('active_ids')
        for x in activeIds:
            self.env['estate.property.offers'].create({'price':self.price ,'partner_id': self.partner_id.id,'property_id':x})
        return True


class tag_wizard(models.TransientModel):
    _name = "tag.wizard"
    _description = "wizard"
    
    tag_id = fields.Many2many('estate.property.tags')

    def action_add_tag(self):
        self.ensure_one()
        activeIds = self.env.context.get('active_ids')
        for x in activeIds:
            a  = self.env['estate.property'].browse(x)#.read({'tags_ids'})
            print("#######################################",a.tags_ids + self.tag_id)
            self.env['estate.property'].browse(x).write({'tags_ids': a.tags_ids + self.tag_id})
        return True