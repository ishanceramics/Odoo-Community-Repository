# -*- coding: utf-8 -*-
#################################################################################
# Author : Your Company
# Copyright(c): 2025-Present Your Company
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#################################################################################

{
    'name': 'Unit Budget Management',
    'version': '1.0.0',
    'summary': 'Manage unit-wise budget allocations',
    'description': '''
        Unit Budget Management Module
        Compatible with Odoo 18 Enterprise Edition
    ''',
    'category': 'Tools',
    'author': 'Your Company',
    'website': 'https://yourcompany.com',
    
    'depends': ['base', 'mail', 'product'],  # Add 'product' dependency
    
    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'views/unit_budget_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}