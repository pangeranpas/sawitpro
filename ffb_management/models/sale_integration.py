# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class SawitSaleIntegration(models.Model):
    _name = 'sawitpro.sale.integration'
    _description = 'Sale Integration Helper (Transient)'

    name = fields.Char('Name')

    def create_sale_from_summaries(self, summary_ids, partner_id=None):
        Sale = self.env['sale.order']
        Product = self.env['product.product']
        PriceModel = self.env['sawitpro.ffb.price']
        if not summary_ids:
            raise UserError('No summaries provided')
        summaries = self.env['sawitpro.daily.summary'].browse(summary_ids)
        grouped = {}
        for s in summaries:
            grouped.setdefault(s.mill_id.id, []).append(s)
        created_orders = []
        product = Product.search([('default_code', '=', 'FFB')], limit=1)
        if not product:
            product = Product.create({
                'name': 'FFB',
                'type': 'service',
                'default_code': 'FFB'
            })
        for mill_id, sums in grouped.items():
            mill = self.env['res.partner'].browse(mill_id)
            partner = partner_id and self.env['res.partner'].browse(partner_id) or mill
            so = Sale.create({
                'partner_id': partner.id,
                'partner_invoice_id': partner.id,
                'partner_shipping_id': partner.id,
                'date_order': fields.Datetime.now()
            })
            for s in sums:
                price = PriceModel.search(
                    [('mill_id', '=', mill_id), ('date', '=', s.date)],
                    limit=1
                )
                unit_price = price.price_per_kg if price else 0.0
                so.order_line.create({
                    'order_id': so.id,
                    'product_id': product.id,
                    'name': 'FFB %s' % s.date,
                    'product_uom_qty': s.total_net_kg,
                    'price_unit': unit_price,
                    'product_uom': product.uom_id.id
                })
                s.sale_order_id = so.id
            so.action_confirm()
            created_orders.append(so)
        return created_orders