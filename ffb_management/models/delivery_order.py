# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SawitDeliveryOrder(models.Model):
    _name = 'sawitpro.delivery.order'
    _description = 'FFB Delivery Order'
    _order = 'scheduled_date desc, id'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='Delivery Order', required=True, copy=False, readonly=True, default=lambda self: 'New')
    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True)
    vendor_type = fields.Selection([('smallholder','Smallholder'),('intermediary','Intermediary')], default='smallholder')
    scheduled_date = fields.Datetime(string='Scheduled Date')
    quantity_kg = fields.Float(string='Quantity (kg)')
    moisture = fields.Float(string='Moisture (%)')
    impurity = fields.Float(string='Impurity (%)')
    quality = fields.Selection([('good','Good'),('med','Medium'),('bad','Bad')], default='good')
    weighbridge_ids = fields.One2many('sawitpro.weighbridge', 'delivery_order_id', string='Weighbridge Receipts')
    trip_id = fields.Many2one('sawitpro.trip', string='Trip')
    fleet_id = fields.Many2one('fleet.vehicle', string='Fleet')
    state = fields.Selection([('draft','Draft'),('assigned','Assigned'),('picked_up','Picked Up'),('delivered','Delivered'),('confirmed','Confirmed'),('cancel','Cancelled')], default='draft')


    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('sawitpro.delivery.order') or 'New'
        return super(SawitDeliveryOrder, self).create(vals)


    def action_assign(self):
        return self.write({'state': 'assigned'})


    def action_mark_picked(self):
        return self.write({'state': 'picked_up'})


    def action_mark_delivered(self):
        return self.write({'state': 'delivered'})


    def action_confirm(self):
        return self.write({'state': 'confirmed'})