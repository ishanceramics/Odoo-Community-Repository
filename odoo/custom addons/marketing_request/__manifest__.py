{
    'name': 'AK Marketing Request',
    'version': '1.0',
    'category': 'Marketing',
    'author': 'Arvind Kumar',
    'summary': 'Marketing Request Management',
    'description': """
        This module allows to manage marketing requests with approval workflow.
    """,
    'depends': ['base', 'mail', 'hr', 'product'],  # Remove 'marketing_campaign_extension' temporarily
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/marketing_request_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3'
}