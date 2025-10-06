from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class ProductCategory(models.Model):
    _inherit = 'product.category'

    has_size = fields.Boolean(string="Has size attribute", help="Does this category have size?")
    packaging_ids = fields.Many2many('wk.product.packaging', string="Packaging", help="Select packaging for this category.")
    
    
    
    


class WkProductCategory(models.Model):
    _name = 'wk.product.category'
    _description = "Product Category"
    
    
    
    name = fields.Char(string="Name", help="Each product category is given a unique name.", required=True)
    description = fields.Text(string="Description", help="Description for product category.")
    
    
    @api.constrains('name')
    def _check_product_category_name(self):
        for rec in self:
            name_count = self.search_count([('name', '=', rec.name), ('id', '!=', rec.id)])
            if name_count > 0:
                raise ValidationError("The name should be unique for each product category!")
        return True
    


class WkProductTypeCategory(models.Model):
    _name = 'wk.product.type.category'
    _description = "Product Type Category"
    
    
    
    name = fields.Char(string="Name", help="Each product type category is given a unique name.", required=True)
    description = fields.Text(string="Description", help="Description for product type category.")
    
    
    @api.constrains('name')
    def _check_product_type_category_name(self):
        for rec in self:
            name_count = self.search_count([('name', '=', rec.name), ('id', '!=', rec.id)])
            if name_count > 0:
                raise ValidationError("The name should be unique for each product type category!")
        return True
class WkProductpackaging(models.Model):
    _name = 'wk.product.packaging'
    _description = "Product Packaging"


    name = fields.Char(string="Name", help="Each product packaging is given a unique name.", required=True)
    description = fields.Text(string="Description", help="Description for product packaging.")
    category_ids = fields.Many2many('product.category', string="Categories", help="Categories that can use this packaging.")
    
    
    @api.constrains('name')
    def _check_product_packaging_name(self):
        for rec in self:
            name_count = self.search_count([('name', '=', rec.name), ('id', '!=', rec.id)])
            if name_count > 0:
                raise ValidationError("The name should be unique for each product packaging!")
        return True
