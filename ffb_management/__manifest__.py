# -*- coding: utf-8 -*-
{
    'name': 'SawitPRO FFB Management',
    'summary': 'Manage FFB deliveries, weighbridge receipts, daily summaries and sales',
    'version': '1.0.0',
    'author': 'Pangeran - Generated',
    'license': 'LGPL-3',
    'category': 'Operations/Inventory',
    'depends': ['base', 'sale_management', 'account', 'fleet', 'product', 'sale'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/delivery_order_views.xml',
        'views/weighbridge_views.xml',
        'views/trip_views.xml',
        'views/daily_summary_views.xml',
        'views/ffb_price_views.xml',
        'views/sale_enhanced_views.xml',
        'views/wizards_views.xml',
        'views/dashboard_views.xml',
        'data/ir_sequence_data.xml',
        'data/cron_jobs.xml',
        ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
}