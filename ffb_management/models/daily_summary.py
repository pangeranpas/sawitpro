# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime

class SawitDailySummary(models.Model):
    _name = 'sawitpro.daily.summary'
    _description = 'Daily Delivery Summary'
    _order = 'date desc'

    name = fields.Char(string='Summary', compute='_compute_name')
    date = fields.Date(required=True, default=fields.Date.context_today)
    mill_id = fields.Many2one('res.partner', string='Mill')
    fleet_id = fields.Many2one('fleet.vehicle', string='Fleet')
    delivery_order_ids = fields.Many2many('sawitpro.delivery.order', string='Delivery Orders')
    total_net_kg = fields.Float(string='Total Net (kg)', compute='_compute_total', store=True)

    def _compute_name(self):
        for rec in self:
            rec.name = '%s - %s - %s' % (
                rec.date or '',
                rec.mill_id.name or 'NoMill',
                rec.fleet_id.name or 'NoFleet'
            )

    @api.depends('delivery_order_ids', 'delivery_order_ids.quantity_kg')
    def _compute_total(self):
        for rec in self:
            rec.total_net_kg = sum(rec.delivery_order_ids.mapped('quantity_kg') or [])

    @api.model
    def create_daily_summaries(self, date=None):
        date = date or fields.Date.context_today(self)
        dt_date = date if isinstance(date, datetime.date) else fields.Date.from_string(date)
        start = datetime.datetime.combine(dt_date, datetime.time.min)
        end = datetime.datetime.combine(dt_date, datetime.time.max)
        dom = [
            ('state', 'in', ('delivered', 'confirmed')),
            ('scheduled_date', '>=', start),
            ('scheduled_date', '<=', end)
        ]
        orders = self.env['sawitpro.delivery.order'].search(dom)
        # Group by mill (vendor's parent as mill) and fleet
        groups = {}
        for o in orders:
            mill = o.vendor_id.parent_id or o.vendor_id
            key = (mill.id, o.fleet_id.id)
            groups.setdefault(key, []).append(o)
        created = []
        for (mill_id, fleet_id), ords in groups.items():
            summary = self.search([
                ('date', '=', dt_date),
                ('mill_id', '=', mill_id),
                ('fleet_id', '=', fleet_id)
            ], limit=1)
            order_ids = [o.id for o in ords]
            if not summary:
                summary = self.create({
                    'date': dt_date,
                    'mill_id': mill_id,
                    'fleet_id': fleet_id,
                    'delivery_order_ids': [(6, 0, order_ids)]
                })
            else:
                summary.delivery_order_ids = [(6, 0, list(set(summary.delivery_order_ids.ids + order_ids)))]
            created.append(summary)
        return created