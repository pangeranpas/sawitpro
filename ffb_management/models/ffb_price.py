# -*- coding: utf-8 -*-
from odoo import models, fields


class SawitFfbPrice(models.Model):
    _name = 'sawitpro.ffb.price'
    _description = 'FFB Daily Price'
    _order = 'date desc'


    mill_id = fields.Many2one('res.partner', string='Mill', required=True)
    date = fields.Date(required=True)
    price_per_kg = fields.Monetary(required=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)


    _sql_constraints = [
    ('unique_mill_date', 'unique(mill_id, date)', 'Price for a mill on a date must be unique')
    ]


    def name_get(self):
        res = []
        for r in self:
            res.append((r.id, '%s - %s : %s' % (r.mill_id.name or 'NoMill', r.date, r.price_per_kg)))
        return res