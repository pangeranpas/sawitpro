# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SawitWeighbridge(models.Model):
    _name = 'sawitpro.weighbridge'
    _description = 'Weighbridge Receipt'

    name = fields.Char(string='Receipt Ref', default=lambda self: 'New')
    delivery_order_id = fields.Many2one('sawitpro.delivery.order', string='Delivery Order')
    weigh_in = fields.Datetime(string='Weigh In')
    weigh_out = fields.Datetime(string='Weigh Out')
    gross_weight_kg = fields.Float('Gross (kg)')
    tare_weight_kg = fields.Float('Tare (kg)')
    net_weight_kg = fields.Float('Net (kg)', compute='_compute_net', store=True)
    vehicle_no = fields.Char('Vehicle No')
    operator = fields.Many2one('res.users', string='Operator')

    @api.depends('gross_weight_kg', 'tare_weight_kg')
    def _compute_net(self):
        for r in self:
            r.net_weight_kg = (r.gross_weight_kg or 0.0) - (r.tare_weight_kg or 0.0)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('sawitpro.weighbridge') or 'New'
        return super(SawitWeighbridge, self).create(vals)