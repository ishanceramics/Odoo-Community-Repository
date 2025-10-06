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




class WkProductFamily(models.Model):
    _name = 'wk.product.family'
    _description = "Product Family"
    
    
    name = fields.Char(string="Name", help="Each product family is given a unique name.", required=True)
    description = fields.Text(string="Description", help="Description for product family.")
    
    
    
    @api.constrains('name')
    def _check_product_family_name(self):
        for rec in self:
            name_count = self.search_count([('name', '=', rec.name), ('id', '!=', rec.id)])
            if name_count > 0:
                raise ValidationError("The name should be unique for each product family!")
        return True
