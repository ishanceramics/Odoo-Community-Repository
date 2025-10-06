from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError, ValidationError
import logging
from . import static_franchisee_management

_logger = logging.getLogger(__name__)

MM_TO_INCH = 25.4   # 1 inch = 25.4mm 



class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    @tools.ormcache()
    def _get_default_category_id(self):
        return self.env['product.category'].search([('parent_id', '=', None)], limit=1).id

    packaging_id = fields.Many2one('wk.product.packaging', string="Packaging", domain="[('category_ids', 'in', [categ_id])]", help="Select packaging for this product.")
    item_code = fields.Char("Item Code", compute="_compute_item_code", inverse="_set_item_code", store=True)
    item_name = fields.Char("Item Name", compute="_compute_item_name", inverse="_set_item_name", store=True)
    item_classification = fields.Selection(static_franchisee_management.ITEM_CLASSIFICATION, string="Item Classification", compute='_compute_item_classification', inverse='_set_item_classification', store=True)
    product_length = fields.Float("Length", compute='_compute_product_length', inverse='_set_product_length', store=True)
    product_width = fields.Float("Width",compute='_compute_product_width', inverse='_set_product_width', store=True)
    product_height = fields.Float("Height", compute='_compute_product_height', inverse='_set_product_height', store=True)
    product_thickness = fields.Float("Thickness", compute='_compute_product_thickness', inverse='_set_product_thickness', store=True)
    product_length_inch = fields.Float("Length(in Inch)", compute='_compute_product_length_inch',)
    product_width_inch = fields.Float("Width(in Inch)",compute='_compute_product_width_inch', )
    product_height_inch = fields.Float("Height(in Inch)", compute='_compute_product_height_inch',)
    product_thickness_inch = fields.Float("Thickness(in Inch)", compute='_compute_product_thickness_inch')
    size_in_mm = fields.Char("Size(in mm)", compute="_compute_size_in_mm",)
    size_in_inch = fields.Char("Size(in Inch)", compute="_compute_size_in_inch")
    area_per_box_sqmtr = fields.Float("Area per Box(in Sq Mtr)", compute="_compute_area_per_box_sq_mtr")
    area_per_box_sqft = fields.Float("Area per Box(in Sq Ft)", compute="_compute_area_per_box_sqft")
    manufacturer_id = fields.Many2one('wk.product.manufacturer', string='Manufacturer', compute='_compute_manufacturer', inverse='_set_manufacturer',store=True)
    product_family_id = fields.Many2one('wk.product.family', string='Family',compute='_compute_product_family', inverse='_set_product_family',store=True)
    product_slab_id = fields.Many2one('wk.product.slab', string='Slab',compute='_compute_product_slab', inverse='_set_product_slab',store=True)
    grade_id = fields.Many2one('wk.product.grade', string='Grade', compute='_compute_grade', inverse='_set_grade',store=True)
    product_series_id = fields.Many2one('wk.product.series', string='Product Series', compute='_compute_product_series', inverse='_set_product_series',store=True)
    brand_id = fields.Many2one('wk.product.brand', string='Brand', compute='_compute_product_brand', inverse='_set_product_brand', store=True)
    brand_type = fields.Selection(related="brand_id.brand_type")
    product_quality_id = fields.Many2one("wk.product.quality", string="Product Quality",compute='_compute_product_quality', inverse='_set_product_quality',store=True)
    vendor_product_quality_id = fields.Many2one("wk.vendor.product.quality", string="Vendor's Product Quality",compute='_compute_vendor_product_quality', inverse='_set_vendor_product_quality',store=True)
    printing_type_id = fields.Many2one("wk.printing.type", string="Printing Type",compute='_compute_printing_type', inverse='_set_printing_type',store=True)
    segment = fields.Selection(static_franchisee_management.SEGMENT, string="Segment",compute='_compute_segment', inverse='_set_segment',store=True)
    product_categ_id = fields.Many2one('wk.product.category', 'Product Category(Category-Based)', change_default=True,)
    prod_type_categ_id = fields.Many2one('wk.product.type.category', 'Product Type Category', change_default=True)
    model_id = fields.Many2one('wk.product.model', 'Model')
    sub_model_id = fields.Many2one('wk.product.submodel', 'Sub-Model')
    body_type = fields.Many2one('wk.product.body.type', 'Body Type', help ="Type of material from which the item is made of.")
    portfolio_id = fields.Many2one('wk.product.portfolio', 'Product Portfolio', domain=[('brand_ids', 'in', [brand_id])], help="Select a portfolio to get default portfolio values.", compute='_compute_product_portfolio', inverse='_set_product_portfolio', store=True)
    product_size_id = fields.Many2one('wk.product.size', 'Product Size', help ="Size of the Product.", compute='_compute_product_size', inverse='_set_product_size',store=True)
    has_size = fields.Boolean(related="categ_id.has_size")
    item_group_id = fields.Many2one('wk.item.group', string='Item Group', compute='_compute_item_group', inverse='_set_item_group',store=True)
    vendor_item_group_id = fields.Many2one('wk.vendor.item.group', string="Vendor's  Item Group", compute='_compute_vendor_item_group', inverse='_set_vendor_item_group',store=True)
    product_color_id = fields.Many2one('wk.product.color', 'Product Color', help ="Color of the Product.", compute='_compute_product_color', inverse='_set_product_color',store=True)
    product_finish_id = fields.Many2one('wk.product.finish', 'Product Finish', help ="Finish of the Product.", compute='_compute_product_finish', inverse='_set_product_finish',store=True)


    @api.onchange('portfolio_id')
    def _get_portfolio_data(self):
        for record in self:
            if record.portfolio_id:
                record.categ_id = record.portfolio_id.categ_id
                record.product_categ_id = record.portfolio_id.product_categ_id
                record.prod_type_categ_id = record.portfolio_id.prod_type_categ_id
                record.model_id = record.portfolio_id.model_id
                record.sub_model_id = record.portfolio_id.sub_model_id
                record.body_type = record.portfolio_id.body_type
                record.product_size_id = record.portfolio_id.product_size_id
            
    
    @api.onchange('product_size_id')
    def _get_product_size(self):
        for record in self:
            if record.product_size_id:
                record.product_length = record.product_size_id.product_length
                record.product_width = record.product_size_id.product_width
                record.product_height = record.product_size_id.product_height
                record.product_thickness = record.product_size_id.product_thickness

    
            
    @api.depends_context('company')
    @api.depends('product_variant_ids.standard_price', 'seller_ids')
    def _compute_standard_price(self):
        for template in self:
            template._compute_template_field_from_variant_field('standard_price', template.standard_price)
            if template.seller_ids:
                supplier_with_no_qty = template.seller_ids.filtered(lambda s: s.min_qty == 0)
                if len(supplier_with_no_qty)>0 and not isinstance(supplier_with_no_qty[0].id, models.NewId):
                    supplier_with_no_qty = supplier_with_no_qty.sorted('id')
                    supplier = supplier_with_no_qty[0]
                    template.standard_price = supplier.price
                    template._set_prod_variant_field('standard_price')
    
    
    
    
    def _set_prod_variant_field(self, fname):
        """Propagate the value of the given field from the templates to their unique variant.

        Only if it's a single variant product.
        It's used to set fields like barcode, weight, volume..

        :param str fname: name of the field whose value should be propagated to the variant.
            (field name must be identical between product.product & product.template models)
        """
        for template in self:
            count = len(template.product_variant_ids)
            if count == 1:
                template.product_variant_ids[fname] = template[fname]
            elif count == 0:
                archived_variants = self.with_context(active_test=False).product_variant_ids
                if len(archived_variants) == 1:
                    archived_variants[fname] = template[fname]
            else:
                for var in template.product_variant_ids:
                    var[fname] = template[fname]


    
    def _prepare_variant_values(self, combination):
        variant_dict = super()._prepare_variant_values(combination)
        variant_dict['portfolio_id'] = self.portfolio_id.id
        variant_dict['brand_id'] = self.brand_id.id
        variant_dict['item_code'] = self.item_code
        variant_dict['item_group_id'] = self.item_group_id.id
        variant_dict['vendor_item_group_id'] = self.vendor_item_group_id.id
        variant_dict['item_name'] = self.item_name
        variant_dict['item_classification'] = self.item_classification
        variant_dict['product_size_id'] = self.product_size_id.id
        variant_dict['grade_id'] = self.grade_id.id
        variant_dict['product_series_id'] = self.product_series_id.id
        variant_dict['product_quality_id'] = self.product_quality_id.id
        variant_dict['vendor_product_quality_id'] = self.vendor_product_quality_id.id
        variant_dict['printing_type_id'] = self.printing_type_id.id
        variant_dict['segment'] = self.segment
        variant_dict['manufacturer_id'] = self.manufacturer_id.id
        variant_dict['product_family_id'] = self.product_family_id.id
        variant_dict['product_slab_id'] = self.product_slab_id.id
        variant_dict['product_length'] = self.product_length
        variant_dict['product_width'] = self.product_width
        variant_dict['product_height'] = self.product_height
        variant_dict['product_thickness'] = self.product_thickness
        return variant_dict
    
    
    def _create_product_variant(self, combination, log_warning=False):
        """
            Overrided the method to add the franchisee related field values in the product 
            variant during variant creation
        """
        
        self.ensure_one()

        Product = self.env['product.product']

        product_variant = self._get_variant_for_combination(combination)
        if product_variant:
            if not product_variant.active and self.has_dynamic_attributes() and self._is_combination_possible(combination):
                product_variant.active = True
            return product_variant

        if not self.has_dynamic_attributes():
            if log_warning:
                _logger.warning('The user #%s tried to create a variant for the non-dynamic product %s.' % (self.env.user.id, self.id))
            return Product

        if not self._is_combination_possible(combination):
            if log_warning:
                _logger.warning('The user #%s tried to create an invalid variant for the product %s.' % (self.env.user.id, self.id))
            return Product

        return Product.sudo().create({
            'product_tmpl_id': self.id,
            'product_template_attribute_value_ids': [(6, 0, combination._without_no_variant_attributes().ids)],
            'portfolio_id':self.portfolio_id.id,
            'brand_id':self.brand_id.id,
            'item_code': self.item_code,
            'item_group_id': self.item_group_id.id,
            'vendor_item_group_id': self.vendor_item_group_id.id,
            'item_name': self.item_name,
            'item_classification': self.item_classification,
            'product_size_id': self.product_size_id.id,
            'grade_id': self.grade_id.id,
            'product_series_id': self.product_series_id.id,
            'product_quality_id': self.product_quality_id.id,
            'vendor_product_quality_id': self.vendor_product_quality_id.id,
            'printing_type_id': self.printing_type_id.id,
            'segment': self.segment,
            'manufacturer_id': self.manufacturer_id.id,
            'product_family_id': self.product_family_id.id,
            'product_slab_id': self.product_slab_id.id,
            'product_length': self.product_length,
            'product_width': self.product_width,
            'product_height': self.product_height,
            'product_thickness': self.product_thickness,
        })
    
        
    @api.depends('product_variant_ids.portfolio_id')
    def _compute_product_portfolio(self):
        for template in self:
            template._compute_template_field_from_variant_field('portfolio_id', template.portfolio_id.id)

    def _set_product_portfolio(self):
        self._set_prod_variant_field('portfolio_id')
    
    @api.depends('product_variant_ids.item_code')
    def _compute_item_code(self):
        for template in self:
            template._compute_template_field_from_variant_field('item_code', template.item_code)

    def _set_item_code(self):
        self._set_prod_variant_field('item_code')
    
    @api.depends('product_variant_ids.item_group_id')
    def _compute_item_group(self):
        for template in self:
            template._compute_template_field_from_variant_field('item_group_id', template.item_group_id.id)

    def _set_item_group(self):
        self._set_prod_variant_field('item_group_id')
        
    @api.depends('product_variant_ids.vendor_item_group_id')
    def _compute_vendor_item_group(self):
        for template in self:
            template._compute_template_field_from_variant_field('vendor_item_group_id', template.vendor_item_group_id.id)

    def _set_vendor_item_group(self):
        self._set_prod_variant_field('vendor_item_group_id')
    
    
    @api.depends('product_variant_ids.item_name')
    def _compute_item_name(self):
        for template in self:
            template._compute_template_field_from_variant_field('item_name', template.item_name)

    def _set_item_name(self):
        self._set_prod_variant_field('item_name')
        
    @api.depends('product_variant_ids.item_classification')
    def _compute_item_classification(self):
        for template in self:
            template._compute_template_field_from_variant_field('item_classification', template.item_classification)

    def _set_item_classification(self):
        self._set_prod_variant_field('item_classification')
        
    
    @api.depends('product_variant_ids.product_size_id')
    def _compute_product_size(self):
        for template in self:
            template._compute_template_field_from_variant_field('product_size_id', template.product_size_id.id)
        

    def _set_product_size(self):
        self._set_prod_variant_field('product_size_id')
        
    
    @api.depends('product_variant_ids.product_color_id')
    def _compute_product_color(self):
        for template in self:
            template._compute_template_field_from_variant_field('product_color_id', template.product_color_id.id)
        

    def _set_product_color(self):
        self._set_prod_variant_field('product_color_id')
        
    
    @api.depends('product_variant_ids.product_finish_id')
    def _compute_product_finish(self):
        for template in self:
            template._compute_template_field_from_variant_field('product_finish_id', template.product_finish_id.id)
        

    def _set_product_finish(self):
        self._set_prod_variant_field('product_finish_id')

    
    @api.depends('product_variant_ids.grade_id')
    def _compute_grade(self):
        for template in self:
            template._compute_template_field_from_variant_field('grade_id', template.grade_id.id)

    def _set_grade(self):
        self._set_prod_variant_field('grade_id')
        
    @api.depends('product_variant_ids.product_series_id')
    def _compute_product_series(self):
        for template in self:
            template._compute_template_field_from_variant_field('product_series_id', template.product_series_id.id)

    def _set_product_series(self):
        self._set_prod_variant_field('product_series_id')
        
    
    @api.depends('product_variant_ids.brand_id')
    def _compute_product_brand(self):
        for template in self:
            template._compute_template_field_from_variant_field('brand_id', template.brand_id.id)

    def _set_product_brand(self):
        self._set_prod_variant_field('brand_id')
    
    
    @api.depends('product_variant_ids.product_quality_id')
    def _compute_product_quality(self):
        for template in self:
            template._compute_template_field_from_variant_field('product_quality_id', template.product_quality_id.id)

    def _set_product_quality(self):
        self._set_prod_variant_field('product_quality_id')
        
    @api.depends('product_variant_ids.vendor_product_quality_id')
    def _compute_vendor_product_quality(self):
        for template in self:
            template._compute_template_field_from_variant_field('vendor_product_quality_id', template.vendor_product_quality_id.id)

    def _set_vendor_product_quality(self):
        self._set_prod_variant_field('vendor_product_quality_id')
        
    @api.depends('product_variant_ids.printing_type_id')
    def _compute_printing_type(self):
        for template in self:
            template._compute_template_field_from_variant_field('printing_type_id', template.printing_type_id.id)

    def _set_printing_type(self):
        self._set_prod_variant_field('printing_type_id')
        
    @api.depends('product_variant_ids.segment')
    def _compute_segment(self):
        for template in self:
            template._compute_template_field_from_variant_field('segment', template.segment)

    def _set_segment(self):
        self._set_prod_variant_field('segment')
        
    @api.depends('product_variant_ids.manufacturer_id')
    def _compute_manufacturer(self):
        for template in self:
            template._compute_template_field_from_variant_field('manufacturer_id', template.manufacturer_id.id)

    def _set_manufacturer(self):
        self._set_prod_variant_field('manufacturer_id')
        
    @api.depends('product_variant_ids.product_family_id')
    def _compute_product_family(self):
        for template in self:
            template._compute_template_field_from_variant_field('product_family_id', template.product_family_id.id)

    def _set_product_family(self):
        self._set_prod_variant_field('product_family_id')
        
    @api.depends('product_variant_ids.product_slab_id')
    def _compute_product_slab(self):
        for template in self:
            template._compute_template_field_from_variant_field('product_slab_id', template.product_slab_id.id)

    def _set_product_slab(self):
        self._set_prod_variant_field('product_slab_id')
    
    @api.depends('product_variant_ids.product_length')
    def _compute_product_length(self):
        for template in self:
            template._compute_template_field_from_variant_field('product_length', template.product_length)
        
    def _set_product_length(self):
        self._set_prod_variant_field('product_length')
        
    @api.depends('product_variant_ids.product_width')
    def _compute_product_width(self):
        for template in self:
            template._compute_template_field_from_variant_field('product_width', template.product_width)
        
    def _set_product_width(self):
        self._set_prod_variant_field('product_width')
        
    @api.depends('product_variant_ids.product_height')
    def _compute_product_height(self):
        for template in self:
            template._compute_template_field_from_variant_field('product_height', template.product_height)
        
    def _set_product_height(self):
        self._set_prod_variant_field('product_height')
    
    @api.depends('product_variant_ids.product_thickness')
    def _compute_product_thickness(self):
        for template in self:
            template._compute_template_field_from_variant_field('product_thickness', template.product_thickness)
        
    def _set_product_thickness(self):
        self._set_prod_variant_field('product_thickness')
                
    @api.depends('product_length')
    def _compute_product_length_inch(self):
        for rec in self:
            if rec.product_length:
                rec.product_length_inch = rec.product_length / MM_TO_INCH
            else:
                rec.product_length_inch = 0
    
    @api.depends('product_width')
    def _compute_product_width_inch(self):
        for rec in self:
            if rec.product_width:
                rec.product_width_inch = rec.product_width / MM_TO_INCH
            else:
                rec.product_width_inch = 0
            
            
    @api.depends('product_height')
    def _compute_product_height_inch(self):
        for rec in self:
            if rec.product_height:
                rec.product_height_inch = rec.product_height / MM_TO_INCH
            else:
                rec.product_height_inch = 0
    
    @api.depends('product_thickness')
    def _compute_product_thickness_inch(self):
        for rec in self:
            if rec.product_thickness:
                rec.product_thickness_inch = rec.product_thickness / MM_TO_INCH
            else:
                rec.product_thickness_inch = 0
        
    
    @api.depends('product_length', 'product_width', 'product_height')
    def _compute_size_in_mm(self):
        for rec in self:
            rec.size_in_mm = ''
            if rec.product_length and rec.product_width:
                rec.size_in_mm = f"{round(rec.product_length, 2)}mm x {round(rec.product_width, 2)}mm"
            if rec.product_length and rec.product_width and rec.product_height:
                rec.size_in_mm = f"{round(rec.product_length, 2)}mm x {round(rec.product_width, 2)}mm x {round(rec.product_height, 2)}mm"
            
    
    @api.depends('product_length_inch', 'product_width_inch', 'product_height_inch')
    def _compute_size_in_inch(self):
        for rec in self:
            rec.size_in_inch = ''
            if rec.product_length_inch and rec.product_width_inch:
                rec.size_in_inch = f"{round(rec.product_length_inch, 2)}in x {round(rec.product_width_inch, 2)}in"
            if rec.product_length_inch and rec.product_width_inch and rec.product_height_inch:
                rec.size_in_inch = f"{round(rec.product_length_inch, 2)}in x {round(rec.product_width_inch, 2)}in x {round(rec.product_height_inch, 2)}in"
        
        
    @api.depends('product_length', 'product_width')
    def _compute_area_per_box_sq_mtr(self):
        for rec in self:
            if rec.product_length and rec.product_width:
                prd_length_mtr = rec.product_length / 1000 
                prd_width_mtr = rec.product_width / 1000
                rec.area_per_box_sqmtr = prd_length_mtr * prd_width_mtr
            else:
                rec.area_per_box_sqmtr = 0
            
            rec._set_prod_variant_field('area_per_box_sqmtr')
                
    @api.depends('product_length_inch', 'product_width_inch')
    def _compute_area_per_box_sqft(self):
        for rec in self:
            if rec.product_length_inch and rec.product_width_inch:
                prd_length_ft = rec.product_length_inch / 12 
                prd_width_ft = rec.product_width_inch / 12
                rec.area_per_box_sqft = prd_length_ft * prd_width_ft
            else:
                rec.area_per_box_sqft = 0
            
            rec._set_prod_variant_field('area_per_box_sqft')
        




class ProductProduct(models.Model):
    _inherit = 'product.product'


    
    item_code = fields.Char("Item Code")
    item_name = fields.Char("Item Name")
    manufacturer_id = fields.Many2one('wk.product.manufacturer', string='Manufacturer',)
    portfolio_id = fields.Many2one('wk.product.portfolio', 'Product Portfolio', help="Select a portfolio to get default portfolio values.")
    item_classification = fields.Selection(static_franchisee_management.ITEM_CLASSIFICATION, string="Item Classification")
    product_family_id = fields.Many2one('wk.product.family', string='Family',)
    product_length = fields.Float("Length")
    product_width = fields.Float("Width")
    product_height = fields.Float("Height")
    product_thickness = fields.Float("Thickness")
    product_length_inch = fields.Float("Length(in Inch)", compute='_compute_product_length',)
    product_width_inch = fields.Float("Width(in Inch)", compute='_compute_product_width',)
    product_height_inch = fields.Float("Height(in Inch)", compute='_compute_product_height',)
    product_thickness_inch = fields.Float("Thickness(in Inch)",compute='_compute_product_thickness',)
    product_slab_id = fields.Many2one('wk.product.slab', string='Slab',)
    area_per_box_sqmtr = fields.Float("Area per Box(in Sq Mtr)", compute="_compute_area_per_box_sq_mtr")
    area_per_box_sqft = fields.Float("Area per Box(in Sq Ft)", compute="_compute_area_per_box_sqft")
    size_in_mm = fields.Char("Size(in mm)", compute="_compute_size_in_mm")
    size_in_inch = fields.Char("Size(in Inch)", compute="_compute_size_in_inch")
    grade_id = fields.Many2one('wk.product.grade', string='Grade',)
    product_series_id = fields.Many2one('wk.product.series', string='Product Series')
    brand_id = fields.Many2one('wk.product.brand', string='Brand')
    brand_type = fields.Selection(related="brand_id.brand_type")
    product_quality_id = fields.Many2one("wk.product.quality", string="Product Quality")
    vendor_product_quality_id = fields.Many2one("wk.vendor.product.quality", string="Vendor's Product Quality")
    printing_type_id = fields.Many2one("wk.printing.type", string="Printing Type")
    segment = fields.Selection(static_franchisee_management.SEGMENT, string="Segment")
    product_size_id = fields.Many2one('wk.product.size', 'Product Size', help ="Size of the Product.")
    item_group_id = fields.Many2one('wk.item.group', string='Item Group')
    vendor_item_group_id = fields.Many2one('wk.vendor.item.group', string="Vendor's Item Group")
    product_color_id = fields.Many2one('wk.product.color', string="Product Color", help ="Color of the Product")
    product_finish_id = fields.Many2one('wk.product.finish', string="Product Finish", help ="Finish of the Product")

    
    @api.onchange('portfolio_id')
    def _get_portfolio_data(self):
        for record in self:
            if record.portfolio_id:
                record.categ_id = record.portfolio_id.categ_id
                record.product_categ_id = record.portfolio_id.product_categ_id
                record.prod_type_categ_id = record.portfolio_id.prod_type_categ_id
                record.model_id = record.portfolio_id.model_id
                record.sub_model_id = record.portfolio_id.sub_model_id
                record.body_type = record.portfolio_id.body_type
                record.product_size_id = record.portfolio_id.product_size_id
    
    
    @api.onchange('product_size_id')
    def _get_product_size(self):
        for record in self:
            if record.product_size_id:
                record.product_length = record.product_size_id.product_length
                record.product_width = record.product_size_id.product_width
                record.product_height = record.product_size_id.product_height
                record.product_thickness = record.product_size_id.product_thickness
    
    @api.depends('product_length')
    def _compute_product_length(self):
        for rec in self:
            if rec.product_length:
                rec.product_length_inch = rec.product_length / MM_TO_INCH
            else:
                rec.product_length_inch = 0
    
    
    @api.depends('product_width')
    def _compute_product_width(self):
        for rec in self:
            if rec.product_width:
                rec.product_width_inch = rec.product_width / MM_TO_INCH
            else:
                rec.product_width_inch = 0
            
            
    @api.depends('product_height')
    def _compute_product_height(self):
        for rec in self:
            if rec.product_height:
                rec.product_height_inch = rec.product_height / MM_TO_INCH
            else:
                rec.product_height_inch = 0
    
    @api.depends('product_thickness')
    def _compute_product_thickness(self):
        for rec in self:
            if rec.product_thickness:
                rec.product_thickness_inch = rec.product_thickness / MM_TO_INCH
            else:
                rec.product_thickness_inch = 0
            
    
    @api.depends('product_length', 'product_width', 'product_height')
    def _compute_size_in_mm(self):
        for rec in self:
            rec.size_in_mm = ''
            if rec.product_length and rec.product_width:
                rec.size_in_mm = f"{round(rec.product_length, 2)}mm x {round(rec.product_width, 2)}mm"
            if rec.product_length and rec.product_width and rec.product_height:
                rec.size_in_mm = f"{round(rec.product_length, 2)}mm x {round(rec.product_width, 2)}mm x {round(rec.product_height, 2)}mm"
                
            
    
    @api.depends('product_length_inch', 'product_width_inch', 'product_height_inch')
    def _compute_size_in_inch(self):
        for rec in self:
            rec.size_in_inch = ''
            if rec.product_length_inch and rec.product_width_inch:
                rec.size_in_inch = f"{round(rec.product_length_inch, 2)}in x {round(rec.product_width_inch, 2)}in"
            if rec.product_length_inch and rec.product_width_inch and rec.product_height_inch:
                rec.size_in_inch = f"{round(rec.product_length_inch, 2)}in x {round(rec.product_width_inch, 2)}in x {round(rec.product_height_inch, 2)}in"
                
    
    
    @api.depends('product_length', 'product_width')
    def _compute_area_per_box_sq_mtr(self):
        for rec in self:
            if rec.product_length and rec.product_width:
                prd_length_mtr = rec.product_length / 1000 
                prd_width_mtr = rec.product_width / 1000
                rec.area_per_box_sqmtr = prd_length_mtr * prd_width_mtr
            else:
                rec.area_per_box_sqmtr = 0
                
    @api.depends('product_length_inch', 'product_width_inch')
    def _compute_area_per_box_sqft(self):
        for rec in self:
            if rec.product_length_inch and rec.product_width_inch:
                prd_length_ft = rec.product_length_inch / 12 
                prd_width_ft = rec.product_width_inch / 12
                rec.area_per_box_sqft = prd_length_ft * prd_width_ft
            else:
                rec.area_per_box_sqft = 0
                
                
                
class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"
    
    
    applied_on = fields.Selection(selection_add=[('4_item_group', "Product Item Group"), ('5_product_slab', "Product Slab")], ondelete={'4_item_group': 'set default', '5_product_slab': 'set default'})
    display_applied_on = fields.Selection(selection_add=[('3_item_group', "Product Item Group"), ('4_product_slab', "Product Slab")], ondelete={'3_item_group': 'set default', '4_product_slab': 'set default'})
    item_group_id = fields.Many2one('wk.item.group', string='Product Item Group')
    product_slab_id = fields.Many2one('wk.product.slab', string='Product Slab')
    
    
    @api.depends('applied_on', 'categ_id', 'product_tmpl_id', 'product_id',  'item_group_id', 'product_slab_id')
    def _compute_name(self):
        super(PricelistItem, self)._compute_name()
        for item in self:
            if item.item_group_id and item.applied_on == '4_item_group':
                item.name = _("Item Group: %s", item.item_group_id.display_name)
            elif item.product_slab_id and item.applied_on == '5_product_slab':
                item.name = _("Product Slab: %s", item.product_slab_id.display_name)
            
    
    @api.onchange('display_applied_on')
    def _onchange_display_applied_on(self):
        for item in self:
            _logger.info("item.display_applied_on: %s", item.display_applied_on)
            if not (item.product_tmpl_id or item.categ_id or item.item_group_id or item.product_slab_id):
                item.update(dict(
                    applied_on='3_global',
                ))
            elif item.display_applied_on == '1_product':
                item.update(dict(
                    applied_on='1_product',
                    categ_id=None,
                    item_group_id=None,
                    product_slab_id=None,
                ))
            elif item.display_applied_on == '2_product_category':
                item.update(dict(
                    product_id=None,
                    product_tmpl_id=None,
                    item_group_id=None,
                    product_slab_id=None,
                    applied_on='2_product_category',
                    product_uom=None,
                ))
            elif item.display_applied_on == '3_item_group':
                item.update(dict(
                    applied_on='4_item_group',
                    categ_id=None,
                    product_id=None,
                    product_tmpl_id=None,
                    product_slab_id=None,
                    product_uom=None,
                ))
            elif item.display_applied_on == '4_product_slab':
                item.update(dict(
                    applied_on='5_product_slab',
                    categ_id=None,
                    product_id=None,
                    product_tmpl_id=None,
                    item_group_id=None,
                    product_uom=None,
                ))
    
    @api.onchange('item_group_id', 'product_slab_id')
    def _onchange_rule_content_custom(self):
        if not self.env.context.get('default_applied_on', False):
            item_group_rules = self.filtered('item_group_id')
            product_slab_rules = self.filtered('product_slab_id')
            item_group_rules.update({'applied_on': '4_item_group'})
            product_slab_rules.update({'applied_on': '5_product_slab'})
            global_rules = self - item_group_rules - product_slab_rules
            global_rules.update({'applied_on': '3_global'})

    
    
    def _is_applicable_for(self, product, qty_in_product_uom):
        """Check if the pricelist item is applicable for the given item_group and product_slab."""
        
        res = super(PricelistItem, self)._is_applicable_for(product, qty_in_product_uom)

        if self.applied_on == "4_item_group":
            if product.item_group_id != self.item_group_id:
                res = False
        elif self.applied_on == "5_product_slab":
            if product.product_slab_id != self.product_slab_id:
                res = False
        return res
