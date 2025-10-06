from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError, ValidationError
import logging


_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    
    def get_domain_primary_distributer(self):
        has_primary_distributor = self.env.company.sudo().primary_distributor_id
        if has_primary_distributor and has_primary_distributor.partner_id:
            domain = [("id","=", has_primary_distributor.partner_id.id)]
        else:
            domain = []
        return domain

    primary_distributor_id = fields.Many2one('res.partner')
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True, change_default=True, tracking=True, check_company=True, domain=get_domain_primary_distributer, help="You can find a vendor by its Name, TIN, Email or Internal Reference.")
    
                
