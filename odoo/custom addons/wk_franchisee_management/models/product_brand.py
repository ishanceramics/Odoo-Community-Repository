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


class WkProductBrand(models.Model):
    _name = 'wk.product.brand'
    _description = "Product Brand"
    
    
    name = fields.Char(string="Name", help="Each product brand is given a unique name.", required=True)
    description = fields.Text(string="Description", help="Description for product brand.")

    brand_type = fields.Selection(static_franchisee_management.BRAND_TYPE, string="Brand Type")
    manufacturer_id = fields.Many2one('wk.product.manufacturer', string="Manufacturer")    
    
    
    