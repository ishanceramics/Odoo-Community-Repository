# -*- coding: utf-8 -*-
#################################################################################
# Author : Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>;
#################################################################################
from odoo import api, fields, models, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class PurchaseRequisitionInherit(models.Model):
    _inherit = "purchase.requisition"
    
    pricing_based_on = fields.Selection([
        ('products', 'Products'), ('item_group', 'Item Group')],
        string='Pricing based on', required=True, default='products')
    
    item_group_line_ids = fields.One2many('purchase.requisition.itemgroup.line', 'requisition_id', string='Item Groups to Purchase', copy=True)
    
    manual_quantity_action = fields.Selection([
        ('show_warning', 'Show Warning Only'), ('has_restriction', 'Restrict It')],
        string='Action for Manual Quantity', required=True, default='show_warning')
    
    @api.onchange('vendor_id')
    def _onchange_vendor(self):
        self = self.with_company(self.company_id)
        if not self.vendor_id:
            self.currency_id = self.env.company.currency_id.id
        else:
            self.currency_id = self.vendor_id.property_purchase_currency_id.id or self.env.company.currency_id.id

        requisitions = self.env['purchase.requisition'].search([
            ('vendor_id', '=', self.vendor_id.id),
            ('state', '=', 'confirmed'),
            ('requisition_type', '=', 'blanket_order'),
            ('company_id', '=', self.company_id.id),
        ])
        if any(requisitions):
            title = _("Warning for %s", self.vendor_id.name)
            message = _("There is already an open blanket order for this supplier. We suggest you complete this open blanket order, instead of creating a new one.")
            warning = {
                'title': title,
                'message': message
            }
            if requisitions.manual_quantity_action == 'has_restriction':
                self.vendor_id = None
            return {'warning': warning}
        
    
    def _compute_item_group_products(self):
        """
            Method to add the products line for the products related to the item groups 
            selected in the item groups line in the blanket orders.
        """
        self.line_ids = None
        itg_lines = self.item_group_line_ids
        itg_products = self.env['product.product'].sudo().search([('purchase_ok', '=', True)])
        vals_list = []
        for line in itg_lines:
            item_group = line.item_group_id
            products = itg_products.filtered(lambda p: p.item_group_id.id == item_group.id)
            for prod in products:
                vals = {
                    'requisition_id': self.id, 
                    'product_id': prod.id,
                    'product_qty': line.product_qty,
                    'price_unit': line.price_unit,
                    'product_description_variants': line.itemgroup_description_variants,
                }
                vals_list.append(vals)
        if len(vals_list) > 0:
            self.env['purchase.requisition.line'].sudo().create(vals_list)
        
        return True
    
    def action_confirm(self):
        self.ensure_one()
        if self.pricing_based_on =='item_group':
            if not self.item_group_line_ids:
                raise UserError(_("You cannot confirm agreement '%s' because there is no item group line.", self.name))
            
            self._compute_item_group_products()
        return super(PurchaseRequisitionInherit, self).action_confirm()
        


    def write(self, vals):
        res = super(PurchaseRequisitionInherit, self).write(vals)
        
        # Functionality to remove the related products line if the item group is removed.
        if self.pricing_based_on == 'products':
            if len(self.item_group_line_ids) > 0:
                self.item_group_line_ids.unlink()
                for requisition_line in self.line_ids:
                    requisition_line.supplier_info_ids.sudo().unlink()
                self.line_ids.unlink()
            
        
        if self.pricing_based_on == 'item_group':
            if not len(self.item_group_line_ids) > 0:
                for requisition_line in self.line_ids:
                    requisition_line.supplier_info_ids.sudo().unlink()
                self.line_ids.unlink()
            else:
                item_groups = self.item_group_line_ids.mapped('item_group_id')
                product_lines = self.line_ids.filtered(lambda l: l.product_id.item_group_id.id not in item_groups.ids)
                for requisition_line in product_lines:
                    requisition_line.supplier_info_ids.sudo().unlink()
                product_lines.unlink()
        
        return res

class PurchaseRequisitionItemGroupLine(models.Model):
    _name = "purchase.requisition.itemgroup.line"
    _inherit = 'analytic.mixin'
    _description = "Item Group Requisition Line"
    _rec_name = 'item_group_id'

    item_group_id = fields.Many2one('wk.item.group', string='Item Group', required=True)
    item_group_uom_id = fields.Many2one(
        'uom.uom', 'Item Group Unit of Measure',
        compute='_compute_product_uom_id', store=True, readonly=False, precompute=True)
    product_qty = fields.Float(string='Quantity', digits='Item Group Unit of Measure')
    itemgroup_description_variants = fields.Char('Custom Description')
    price_unit = fields.Float(string='Unit Price', digits='Item Group Price')
    requisition_id = fields.Many2one('purchase.requisition', required=True, string='Purchase Agreement', ondelete='cascade')
    company_id = fields.Many2one('res.company', related='requisition_id.company_id', string='Company', store=True, readonly=True)
    
    
    @api.depends('requisition_id')
    def _compute_product_uom_id(self):
        uom_id = self.env['uom.uom'].sudo().search([('name', '=', 'Units')], limit=1)
        for line in self:
            line.item_group_uom_id = uom_id.id if uom_id else None

