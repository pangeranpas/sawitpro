# -*- coding: utf-8 -*-
from odoo import models, fields, api
import base64, io, csv
from odoo.exceptions import UserError

class SawitBulkImport(models.TransientModel):
    _name = 'sawitpro.bulk.import'
    _description = 'Bulk Import Delivery Orders + Weighbridge'

    file = fields.Binary('CSV File', required=True)
    filename = fields.Char('Filename')

    def action_import(self):
        if not self.file:
            raise UserError('Please provide a CSV file')
        data = base64.b64decode(self.file)
        stream = io.StringIO(data.decode('utf-8'))
        reader = csv.DictReader(stream)
        partner_obj = self.env['res.partner']
        delivery_obj = self.env['sawitpro.delivery.order']
        weigh_obj = self.env['sawitpro.weighbridge']
        errors = []
        created_orders = []
        for i, row in enumerate(reader, start=1):
            try:
                ref = row.get('vendor_external_id') or ''
                name = row.get('vendor_name') or 'Unknown'
                partner = partner_obj.search([('ref','=',ref)], limit=1)
                if not partner:
                    partner = partner_obj.create({'name': name, 'ref': ref})
                do_vals = {
                    'vendor_id': partner.id,
                    'vendor_type': row.get('vendor_type','smallholder'),
                    'scheduled_date': row.get('scheduled_date'),
                    'quantity_kg': float(row.get('quantity_kg') or 0.0),
                    'quality': row.get('quality','good'),
                }
                do = delivery_obj.create(do_vals)
                created_orders.append(do.id)
                # create weighbridge if present
                if row.get('gross_kg') or row.get('tare_kg'):
                    w_vals = {
                        'delivery_order_id': do.id,
                        'weigh_in': row.get('weigh_in'),
                        'weigh_out': row.get('weigh_out'),
                        'gross_weight_kg': float(row.get('gross_kg') or 0.0),
                        'tare_weight_kg': float(row.get('tare_kg') or 0.0),
                        'vehicle_no': row.get('vehicle_no'),
                    }
                    weigh_obj.create(w_vals)
            except Exception as e:
                errors.append((i, str(e)))
        if errors:
            msg = '\n'.join(['Line %s: %s' % (ln, err) for ln, err in errors])
            raise UserError('Some rows failed:\n%s' % msg)
        return {'type': 'ir.actions.act_window_close'}