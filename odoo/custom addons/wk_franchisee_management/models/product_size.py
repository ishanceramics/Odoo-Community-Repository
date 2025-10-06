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
from odoo.exceptions import ValidationError




class WkProductSeries(models.Model):
    _name = 'wk.product.size'
    _description = "Product Size"
    
    
    name = fields.Char(string="Name", help="Each product series is given a unique name.", required=True)
    product_length = fields.Float("Length", help="Length of the Product(in mm)")
    product_width = fields.Float("Width", help="Width of the Product(in mm)")
    product_height = fields.Float("Height", help="Height of the Product(in mm)")
    product_thickness = fields.Float("Thickness", help="Thickness of the Product(in mm)")
    description = fields.Text(string="Description", help="Description for product series.")
    
    
    
    @api.constrains('name')
    def _check_product_size_name(self):
        for rec in self:
            name_count = self.search_count([('name', '=', rec.name), ('id', '!=', rec.id)])
            if name_count > 0:
                raise ValidationError("The name should be unique for each product series!")
        return True
