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

import logging

from odoo import models, fields, api, _

from . import static_franchisee_management

_logger = logging.getLogger(__name__)


class WkFieldValues(models.Model):
    _name = 'wk.field.values'
    _description = "Wk Field Values"
    _rec_name = "field_value"

    field_type = fields.Selection(static_franchisee_management.FIELD_TYPE,
                                  string="Field Type", help="Type of the field.", required=True)
    field_value = fields.Char(string="Field Value",
                              help="Value of the field type.", required=True)
    sequence = fields.Integer()
