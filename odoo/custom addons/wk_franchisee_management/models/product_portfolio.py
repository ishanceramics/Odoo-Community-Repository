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
from odoo import _, api, fields, models, tools
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError, ValidationError




class WkProductPortfolio(models.Model):
    _name = 'wk.product.portfolio'
    _description = "Product Portfolio"

    @tools.ormcache()
    def _get_default_category_id(self):
        return self.env['product.category'].search([('parent_id', '=', None)], limit=1).id
    
    name = fields.Char(string="Portfolio No", default='New', help="Each unique portfolio is given a portfolio no. and auto generated", required=True)
    categ_id = fields.Many2one('product.category', 'Category',change_default=True, default=_get_default_category_id, group_expand='_read_group_categ_id', required=True)
    product_categ_id = fields.Many2one('wk.product.category', 'Product Category', change_default=True,)
    prod_type_categ_id = fields.Many2one('wk.product.type.category', 'Product Type Category', change_default=True)
    model_id = fields.Many2one('wk.product.model', 'Model')
    sub_model_id = fields.Many2one('wk.product.submodel', 'Sub-Model')
    body_type = fields.Many2one('wk.product.body.type', 'Body Type', help ="Type of material from which the item is made of.")
    product_size_id = fields.Many2one('wk.product.size', 'Product Size', help ="Size of the Product.")
    portfolio_old_no = fields.Char('Portfolio Old No.', help ="Old No. of the Portfolio.")
    vendor_ids = fields.Many2many('res.partner', string="Vendors", )
    commitments = fields.Selection([('instock', 'In Stock'), ('againstorder', 'Against Order'), ('moq', 'MOQ Commitments')])
    brand_ids = fields.Many2many('wk.product.brand', string='Brands', required=True)
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('wk.product.portfolio')
        return super(WkProductPortfolio, self).create(vals_list)
