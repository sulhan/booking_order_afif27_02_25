# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Booking Order Afif 27 02 25',
    'version': '1.0',
    'summary': 'Modul untuk mengelola booking order dan work order',
    'category': 'Sales',
    'author': 'Afif',
    'depends': ['base', 'sale', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'views/service_team_views.xml',
        'views/sale_order1_views.xml',
        'views/work_order_report_action.xml', 
        'views/work_order_report.xml',
        'views/work_order_views.xml',
        
        
        'views/menu_views.xml', 
       
       
    ],
    'installable': True,
    'application': True,
    
    
}
