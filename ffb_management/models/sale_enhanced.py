# sawitpro/ffb_management/models/sale_enhanced.py
from odoo import models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_view_daily_summaries(self):
        self.ensure_one()
        return {
            "name": "Daily Delivery Summaries",
            "type": "ir.actions.act_window",
            "res_model": "sawitpro.daily.summary",
            "view_mode": "list,form",
            "domain": [("sale_order_id", "=", self.id)],
            "target": "current",
        }
