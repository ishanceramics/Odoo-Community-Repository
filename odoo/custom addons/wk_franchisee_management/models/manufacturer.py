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
from . import static_franchisee_management




class WkProductManufacturer(models.Model):
    _name = 'wk.product.manufacturer'
    _description = "Product Manufacturer"
    
    
    name = fields.Char(string="Name", help="Each manufacturer is given a unique name.", required=True)
    description = fields.Text(string="Description", help="Description for product manufacturers.")
    brand_ids = fields.One2many('wk.product.brand', 'manufacturer_id', string='Brands')
    
    
    @api.constrains('name')
    def _check_product_manufacturer_name(self):
        for rec in self:
            name_count = self.search_count([('name', '=', rec.name), ('id', '!=', rec.id)])
            if name_count > 0:
                raise ValidationError("The name should be unique for each product manufacturer!")
        return True
