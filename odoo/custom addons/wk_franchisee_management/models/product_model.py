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



class WkProductModel(models.Model):
    _name = 'wk.product.model'
    _description = "Product Model"
    
    
    name = fields.Char(string="Name", help="Each product model is given a unique name.", required=True)
    description = fields.Text(string="Description", help="Description for product model.")
    
    @api.constrains('name')
    def _check_product_model_name(self):
        for rec in self:
            name_count = self.search_count([('name', '=', rec.name), ('id', '!=', rec.id)])
            if name_count > 0:
                raise ValidationError("The name should be unique for each product model!")
        return True
    


class WkProductSubmodel(models.Model):
    _name = 'wk.product.submodel'
    _description = "Product Sub-Model"
    
    
    name = fields.Char(string="Name", help="Each product submodel is given a unique name.", required=True)
    description = fields.Text(string="Description", help="Description for product submodel.")
    # model_id = fields.Many2one('wk.product.model', string="Parent Model", help="Parent Model for product submodel.")
    
    @api.constrains('name')
    def _check_product_submodel_name(self):
        for rec in self:
            name_count = self.search_count([('name', '=', rec.name), ('id', '!=', rec.id)])
            if name_count > 0:
                raise ValidationError("The name should be unique for each product sub-model!")
        return True


class WkProductQuality(models.Model):
    _name = 'wk.product.quality'
    _description = "Product Quality"
    
    
    name = fields.Char(string="Name", help="Each product quality is given a unique name.", required=True)
    description = fields.Text(string="Description", help="Description for product quality.")
    
    @api.constrains('name')
    def _check_product_quality(self):
        for rec in self:
            name_count = self.search_count([('name', '=', rec.name), ('id', '!=', rec.id)])
            if name_count > 0:
                raise ValidationError("The name should be unique for each product quality!")
        return True


class WkVendorProductQuality(models.Model):
    _name = 'wk.vendor.product.quality'
    _description = "Vendor's Product Quality"
    
    
    name = fields.Char(string="Name", help="Each vendor's product quality is given a unique name.", required=True)
    description = fields.Text(string="Description", help="Description for vendor's product quality.")
    
    @api.constrains('name')
    def _check_vendor_product_quality(self):
        for rec in self:
            name_count = self.search_count([('name', '=', rec.name), ('id', '!=', rec.id)])
            if name_count > 0:
                raise ValidationError("The name should be unique for each vendor's product quality!")
        return True


class WkPrintingType(models.Model):
    _name = 'wk.printing.type'
    _description = "Printing Type"
    
    
    name = fields.Char(string="Name", help="Each printing type is given a unique name.", required=True)
    description = fields.Text(string="Description", help="Description for product printing type.")
    
    @api.constrains('name')
    def _check_printing_type(self):
        for rec in self:
            name_count = self.search_count([('name', '=', rec.name), ('id', '!=', rec.id)])
            if name_count > 0:
                raise ValidationError("The name should be unique for each printing type!")
        return True
    
    

class WkProductColor(models.Model):
    _name = 'wk.product.color'
    _description = "Product Color"
    
    
    name = fields.Char(string="Name", help="Each product color is given a unique name.", required=True)
    description = fields.Text(string="Description", help="Description for product color.")
    
    @api.constrains('name')
    def _check_product_color(self):
        for rec in self:
            name_count = self.search_count([('name', '=', rec.name), ('id', '!=', rec.id)])
            if name_count > 0:
                raise ValidationError("The name should be unique for each product color!")
        return True



class WkProductColor(models.Model):
    _name = 'wk.product.color'
    _description = "Product Color"
    
    
    name = fields.Char(string="Name", help="Each product color is given a unique name.", required=True)
    description = fields.Text(string="Description", help="Description for product color.")
    
    @api.constrains('name')
    def _check_product_color(self):
        for rec in self:
            name_count = self.search_count([('name', '=', rec.name), ('id', '!=', rec.id)])
            if name_count > 0:
                raise ValidationError("The name should be unique for each product color!")
        return True


class WkProductFinish(models.Model):
    _name = 'wk.product.finish'
    _description = "Product Finish"
    
    
    name = fields.Char(string="Name", help="Each product finish is given a unique name.", required=True)
    description = fields.Text(string="Description", help="Description for product finish.")
    
    @api.constrains('name')
    def _check_product_finish(self):
        for rec in self:
            name_count = self.search_count([('name', '=', rec.name), ('id', '!=', rec.id)])
            if name_count > 0:
                raise ValidationError("The name should be unique for each product finish!")
        return True
