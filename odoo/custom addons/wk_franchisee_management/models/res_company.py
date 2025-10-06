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
from odoo.exceptions import UserError
from . import static_franchisee_management

class ResCompanyInherit(models.Model):
    _inherit = "res.company"
    
    
    
    
    @api.depends('primary_distributor_id')
    def _set_distributor_data(self):
        portfolios = self.env['wk.product.portfolio'].sudo().search([])
        products = self.env['product.product'].sudo().search([])
        for company in self:
            if company.franchisee_level == 'level_2':
                dist_portfolios = company.primary_distributor_id.portfolio_ids if company.primary_distributor_id else portfolios
                dist_products = company.primary_distributor_id.prod_prod_ids if company.primary_distributor_id else products
                prod_prods = company.prod_prod_ids.filtered(lambda p: p.id in dist_products.ids)
                frnchisee_prtf = company.portfolio_ids.filtered(lambda p: p.id in dist_portfolios.ids)
                company.write({
                    'distributor_portfolio_ids': [(6, 0, dist_portfolios.ids)], 
                    'distributor_product_ids': [(6, 0, dist_products.ids)], 
                    'prod_prod_ids': [(6, 0, prod_prods.ids)] if len(prod_prods) > 0 else None, 
                    'portfolio_ids': [(6, 0, frnchisee_prtf.ids)] if len(frnchisee_prtf) > 0 else None 
                })
            else:
                company.write({
                    'distributor_portfolio_ids': [(6, 0, portfolios.ids)], 
                    'distributor_product_ids': [(6, 0, products.ids)], 
                })
            
            
            if len(company.portfolio_ids) > 0:
                pf_prod_variants = self.prod_prod_ids.filtered(lambda pv: pv.product_tmpl_id.portfolio_id.id in company.portfolio_ids.ids)
                company.write({
                    'prod_prod_ids': [(6, 0, pf_prod_variants.ids)] if len(pf_prod_variants) > 0 else None,  
                })
            else:
                company.write({
                    'prod_prod_ids': None,  
                })
                
    
    
    franchisee_unit_template_id = fields.Many2one('franchisee.unit.template', string="Franchisee Unit",)
    unit_type = fields.Selection(related="franchisee_unit_template_id.unit_type")
    display_area_req = fields.Float(string="Display Area Required(In Sq. ft.)")
    warehouse_area_req = fields.Float(string="Warehouse Area Required(In Sq. ft.)")
    proposed_investment = fields.Float(string="Proposed Investment")
    no_of_employees_req = fields.Integer(string="No. of Employees Required")
    software_license_req = fields.Integer(related="franchisee_unit_template_id.software_license_req")
    projected_sales = fields.Float(related="franchisee_unit_template_id.projected_sales")
    prop_sales_mix_ratio = fields.Char(related="franchisee_unit_template_id.prop_sales_mix_ratio")
    prop_franchisee_margin = fields.Char(related="franchisee_unit_template_id.prop_franchisee_margin")
    franchise_fee = fields.Float(related="franchisee_unit_template_id.franchise_fee")
    is_inventory = fields.Selection(related="franchisee_unit_template_id.is_inventory")
    franchisee_level = fields.Selection(related="franchisee_unit_template_id.franchisee_level")

    display_area_req_deviation = fields.Float(string="Display Area Required Daviation", compute="_set_display_area_req_daviation")
    display_area_req_deviation_number = fields.Char(string="Display Area Required Daviation Number", compute="_set_display_area_req_daviation")
    warehouse_area_req_deviation = fields.Float(string="Warehouse Area Required Daviation", compute="_set_warehouse_area_req_daviation")
    warehouse_area_req_deviation_number = fields.Char(string="Warehouse Area Required Daviation Number", compute="_set_warehouse_area_req_daviation")
    proposed_investment_deviation = fields.Float(string="Proposed Investment Daviation", compute="_set_proposed_investment_daviation")
    proposed_investment_deviation_number = fields.Char(string="Proposed Investment Daviation Number", compute="_set_proposed_investment_daviation")
    primary_distributor_id = fields.Many2one('res.company', string='Primary Distributor(Vendor)')
    portfolio_ids = fields.Many2many('wk.product.portfolio', string="Product Portfolios",)
    prod_prod_ids = fields.Many2many('product.product', string="Product Variants")
    distributor_portfolio_ids = fields.Many2many('wk.product.portfolio', compute="_set_distributor_data", string="Distributor Portfolios")
    distributor_product_ids = fields.Many2many('product.product', compute="_set_distributor_data", string="Distributor Products")
    
    
    
    
    


    @api.onchange('franchisee_unit_template_id')
    def franchisee_unit_template_id_change(self):
        if self.franchisee_unit_template_id:
            self.display_area_req = self.franchisee_unit_template_id.display_area_req
            self.warehouse_area_req = self.franchisee_unit_template_id.warehouse_area_req
            self.proposed_investment = self.franchisee_unit_template_id.proposed_investment
            self.no_of_employees_req = self.franchisee_unit_template_id.no_of_employees_req
            self.primary_distributor_id = 1 if self.franchisee_unit_template_id.franchisee_level=='level_1' else None


    @api.depends('display_area_req')
    def _set_display_area_req_daviation(self):
        for rec in self:

            if rec.display_area_req and rec.franchisee_unit_template_id:
                initial_dar = rec.franchisee_unit_template_id.display_area_req
                dar_daviation = ((rec.display_area_req - initial_dar)/initial_dar) if initial_dar else 0
                rec.display_area_req_deviation_number = '{:+}'.format(rec.display_area_req - initial_dar) if rec.display_area_req - initial_dar > 0 else '{:-}'.format(rec.display_area_req - initial_dar) if rec.display_area_req - initial_dar < 0 else '0'
                rec.display_area_req_deviation = dar_daviation
            else:
                rec.display_area_req_deviation = 0
                rec.display_area_req_deviation_number = '0'


    @api.depends('warehouse_area_req')
    def _set_warehouse_area_req_daviation(self):
        for rec in self:
            if rec.warehouse_area_req and rec.franchisee_unit_template_id:
                initial_war = rec.franchisee_unit_template_id.warehouse_area_req
                war_daviation = ((rec.warehouse_area_req - initial_war)/initial_war) if initial_war else 0
                rec.warehouse_area_req_deviation_number = '{:+}'.format(rec.warehouse_area_req - initial_war) if rec.warehouse_area_req - initial_war > 0 else '{:-}'.format(rec.warehouse_area_req - initial_war) if rec.warehouse_area_req - initial_war < 0 else '0'
                rec.warehouse_area_req_deviation = war_daviation
            else:
                rec.warehouse_area_req_deviation = 0
                rec.warehouse_area_req_deviation_number = '0'


    @api.depends('proposed_investment')
    def _set_proposed_investment_daviation(self):
        for rec in self:
            if rec.proposed_investment and rec.franchisee_unit_template_id:
                initial_pi = rec.franchisee_unit_template_id.proposed_investment
                pi_daviation = ((rec.proposed_investment - initial_pi)/initial_pi) if initial_pi else 0
                rec.proposed_investment_deviation_number = '{:+}'.format(rec.proposed_investment - initial_pi) if rec.proposed_investment - initial_pi > 0 else '{:-}'.format(rec.proposed_investment - initial_pi) if rec.proposed_investment - initial_pi < 0 else '0'
                rec.proposed_investment_deviation = pi_daviation
            else:
                rec.proposed_investment_deviation = 0
                rec.proposed_investment_deviation_number = '0'




class ResPartnerInherit(models.Model):
    _inherit = "res.partner"


    trade_type = fields.Selection(static_franchisee_management.TRADE_TYPE, string="Trade Type", help="Trade Type.")
    product_portfolio_ids = fields.Many2many('wk.product.portfolio', string="Product Portfolios")
    product_supplier_ids = fields.One2many('product.supplierinfo', 'partner_id', string='Product Suppliers Info')
    segment = fields.Selection(static_franchisee_management.SEGMENT, string="Segment")



class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"


    vendor_item_group_id = fields.Many2one("wk.vendor.item.group", string="Item Group")
    vendor_product_quality_id = fields.Many2one("wk.vendor.product.quality", string="Quality")
    product_portfolio_ids = fields.Many2many(related="partner_id.product_portfolio_ids")
