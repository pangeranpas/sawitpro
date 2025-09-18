# -*- coding: utf-8 -*-
from odoo import models, fields

class SawitCreateSalesWizard(models.TransientModel):
    _name = 'sawitpro.create.sales.wizard'
    _description = 'Create Sales from Daily Summaries'

    summary_ids = fields.Many2many('sawitpro.daily.summary', string='Daily Summaries')
    partner_id = fields.Many2one('res.partner', string='Customer (optional)')

    def action_create_sales(self):
        integration = self.env['sawitpro.sale.integration'].create({})
        orders = integration.create_sale_from_summaries(self.summary_ids.ids, partner_id=self.partner_id and self.partner_id.id or None)
        return {
            'type':'ir.actions.act_window',
            'name':'Sales Created',
            'res_model':'sale.order',
            'view_mode':'list,form',
            'domain':[('id','in',[o.id for o in orders])]
        }