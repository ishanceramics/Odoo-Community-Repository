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


class FranchiseeUnitTemplate(models.Model):
    _name = 'franchisee.unit.template'
    _description = "Franchisee Unit Template"

    @api.model
    def _get_currency(self):
        """
            Method to get the user's company currency
        """
        return self.env.user.company_id.currency_id.id

    code = fields.Char(string="Franchisee Code", readonly=True, copy=False)
    name = fields.Char(string="Unit Name", help="Name of the franchisee unit.", required=True)
    unit_type = fields.Selection(static_franchisee_management.UNIT_TYPE, string="Unit Type", required=True, help="Type of the franchisee unit.")
    display_area_req = fields.Float(string="Display Area Required(In Sq. ft.)", help="Required display area of the franchisee unit.")
    warehouse_area_req = fields.Float(string="Warehouse Area Required(In Sq. ft.)", help="Required warehouse area of the franchisee unit.")
    proposed_investment = fields.Float(string="Proposed Investment", help="Proposed Investment for the franchisee unit.")
    no_of_employees_req = fields.Integer(string="No. of Employees Required", help="Required employees for the franchisee unit.")
    software_license_req = fields.Integer(string="Software License Required", help="Required software license for the franchisee unit.")
    projected_sales = fields.Float(string="Projected Sales", help="Projected Sales the franchisee unit.")
    prop_sales_mix_ratio = fields.Char(string="Proposed Sales Mixed Ratio", help="Proposed Sales Mixed Ratio for the franchisee unit.")
    prop_franchisee_margin = fields.Char(string="Proposed Franchisee Margin", help="Proposed Franchisee Margin for the franchisee unit.")
    franchise_fee = fields.Float(string="Franchisee Fee", help="Franchisee Fee for the franchisee unit.")
    is_inventory = fields.Selection(static_franchisee_management.INVENTORY, string="Inventory", help="Inventory for the franchisee unit.")
    franchisee_level = fields.Selection(static_franchisee_management.FRANCHISEE_LEVEL,string="Level", help="Franchisee Level for the franchisee unit.")
    currency_id = fields.Many2one(comodel_name="res.currency", default=_get_currency, help="Default currency for the franchisee unit.")
    segment = fields.Selection(static_franchisee_management.SEGMENT, string="Segment", required=True)
    showroom_location_id = fields.Many2one("wk.field.values", "Showroom Location", domain=[('field_type','=','showroom_location')], ondelete='restrict')
    warehouse_location_id = fields.Many2one("wk.field.values", "Warehouse Location", domain=[('field_type','=','warehouse_location')], ondelete='restrict')
    working_area_id = fields.Many2one("wk.field.values", "Working Area", domain=[('field_type','=','working_area')], ondelete='restrict')
    covering_area_id = fields.Many2one("wk.field.values", "Covering Area", domain=[('field_type','=','covering_area')], ondelete='restrict')
    product_category_ids = fields.Many2many('product.category',string="Product Category", required=True)
    total_area = fields.Integer(string="Total Area")

    def get_selection_label(self, object, field_name, field_value):
        return _(dict(self.env[object].fields_get(allfields=[field_name])[field_name]['selection'])[field_value])

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['code'] = self._generate_franchisee_code(vals)
        return super(FranchiseeUnitTemplate, self).create(vals_list)

    def write(self, vals):
        # Only generate code if it's empty
        for record in self:
            if not record.code:
                vals['code'] = self._generate_franchisee_code(vals)
        return super(FranchiseeUnitTemplate, self).write(vals)

    def _generate_franchisee_code(self, vals):
        """Generate a unique franchisee code based on unit type and sequence"""
        unit_type = vals.get('unit_type', 'other')
        
        # Get the prefix based on unit type
        prefix = dict(static_franchisee_management.UNIT_TYPE).get(unit_type, 'FR')[:2].upper()
        
        # Find last code for this prefix
        last_unit = self.search([
            ('code', '=like', f'{prefix}%'),
        ], order='code desc', limit=1)
        
        next_number = 1
        if last_unit and last_unit.code:
            try:
                next_number = int(last_unit.code[2:]) + 1
            except ValueError:
                next_number = 1
                
        return f"{prefix}{next_number:04d}"

    @api.depends('franchisee_level')
    def _compute_display_name(self):
        for unit in self:
            if unit.franchisee_level:
                unit.display_name = f"{unit.code or ''} - {unit.name}({unit.get_selection_label('franchisee.unit.template', 'franchisee_level', unit.franchisee_level)})"
            else:
                unit.display_name = f"{unit.code or ''} - {unit.name}"

