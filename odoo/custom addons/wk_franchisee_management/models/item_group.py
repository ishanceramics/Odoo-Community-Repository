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
from odoo import models,fields,api,_
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError, ValidationError


class WkItemGroup(models.Model):
    _name = 'wk.item.group'
    _description = "Item Group"
    
    
    name = fields.Char(string="Name", help="Each item group is given a unique name.", required=True)
    description = fields.Text(string="Description", help="Description for item group.")
    product_ids = fields.One2many('product.template', 'item_group_id', string="Related Product Templates")
    product_product_ids = fields.One2many('product.product', 'item_group_id', string="Related Products")
    
    @api.constrains('name')
    def _check_item_group_name(self):
        for rec in self:
            name_count = self.search_count([('name', '=', rec.name), ('id', '!=', rec.id)])
            if name_count > 0:
                raise ValidationError("The name should be unique for each item group!")
        return True
    
    
    
class WkVendorItemGroup(models.Model):
    _name = 'wk.vendor.item.group'
    _description = "Vendor Item Group"
    
    
    name = fields.Char(string="Name", help="Each vendor item group is given a unique name.", required=True)
    description = fields.Text(string="Description", help="Description for vendor item group.")
    
    
    @api.constrains('name')
    def _check_vendor_item_group_name(self):
        for rec in self:
            name_count = self.search_count([('name', '=', rec.name), ('id', '!=', rec.id)])
            if name_count > 0:
                raise ValidationError("The name should be unique for each vendors item group!")
        return True
