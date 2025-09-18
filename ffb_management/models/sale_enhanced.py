# sawitpro/ffb_management/models/sale_enhanced.py
from odoo import models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_view_daily_summaries(self):
        """Buka daftar ringkasan harian yang berelasi dengan Sales Order ini."""
        self.ensure_one()
        return {
            "name": "Daily Delivery Summaries",
            "type": "ir.actions.act_window",
            "res_model": "sawitpro.daily.summary",  # ganti jika model Anda beda
            "view_mode": "list,form",
            # contoh domain jika ada relasi Many2one sale_order_id di summary:
            # "domain": [("sale_order_id", "=", self.id)],
            "domain": [],
            "target": "current",
        }
