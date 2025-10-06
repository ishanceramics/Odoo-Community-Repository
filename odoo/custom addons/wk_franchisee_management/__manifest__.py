# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
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
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "Franchisee Management",
  "summary"              :  """Franchisee Management for odoo E-commerce store""",
  "category"             :  "Marketing",
  "version"              :  "1.1.2",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/",
  "description"          :  """Odoo Extension for managing Franchisee for odoo E-commerce store""",
  "depends"              :  [
                              'base',
                              'mail',
                              'product',
                              'sale',
                              'purchase_requisition_sale',
                            ],
  "data"                 :  [
                              'security/franchisee_security.xml',
                              'security/ir.model.access.csv',
                              'data/portfolio_sequence.xml',
                              'data/wk_field_values_data.xml',
                              'views/res_company_inherit_view.xml',
                              'views/product_inherit_view.xml',
                              'views/product_category_inherit.xml',
                              'views/franchisee_unit_template_views.xml',
                              'views/franchise_product_portfolio.xml',
                              'views/product_specification_fields_views.xml',
                              'views/purchase_requisition_view.xml',
                              'views/wk_field_values_view.xml',
                            ],
  "assets"              :  {
    "web.assets_backend"  :  [],
    "web.assets_frontend" :  []
  },

  "demo"                 :  [],
  "images"               :  [],
  "application"          :  True,
  "installable"          :  True,
}
