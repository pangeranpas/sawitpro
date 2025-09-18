# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SawitTrip(models.Model):
    _name = 'sawitpro.trip'
    _description = 'Trip'

    name = fields.Char(string='Trip Ref', required=True, default=lambda self: 'New')
    planned_date = fields.Date(string='Planned Date')
    fleet_id = fields.Many2one('fleet.vehicle', string='Fleet')
    delivery_order_ids = fields.One2many('sawitpro.delivery.order', 'trip_id', string='Delivery Orders')
    state = fields.Selection([('planned','Planned'),('assigned','Assigned'),('executing','Executing'),('completed','Completed'),('cancel','Cancelled')], default='planned')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('sawitpro.trip') or 'New'
        return super(SawitTrip, self).create(vals)

    def action_assign(self):
        for trip in self:
            trip.delivery_order_ids.write({'state': 'assigned', 'fleet_id': trip.fleet_id.id})
        self.write({'state': 'assigned'})

    def action_start(self):
        for trip in self:
            trip.delivery_order_ids.write({'state': 'picked_up'})
        self.write({'state': 'executing'})

    def action_complete(self):
        for trip in self:
            trip.delivery_order_ids.write({'state': 'delivered'})
        self.write({'state': 'completed'})