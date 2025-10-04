# -*- coding: utf-8 -*-
#################################################################################
# Author : Your Company
# Copyright(c): 2025-Present Your Company
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#################################################################################

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class UnitBudgetLine(models.Model):
    _name = 'unit.budget.line'
    _description = 'Unit Budget Line'
    _rec_name = 'display_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # ADD THIS LINE

    budget_id = fields.Many2one(
        'unit.budget',
        string='Budget',
        required=True,
        ondelete='cascade'
    )
    
    allocation_type = fields.Selection([
        ('store', 'Store Promotion'),
        ('product', 'Product Promotion'),
        ('influencer', 'Influencer Promotion'),
    ], string='Allocation Type', required=True)
    
    month = fields.Selection([
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ], string='Month', required=True)
    
    amount = fields.Float(
        string='Budget Amount',
        required=True,
        help="Allocated budget amount for this type and month",
        tracking=True  # ADD TRACKING
    )
    
    utilized_amount = fields.Float(
        string='Utilized Amount',
        default=0.0,
        help="Amount of budget already utilized",
        tracking=True  # ADD TRACKING
    )
    
    remaining_amount = fields.Float(
        string='Remaining Amount',
        compute='_compute_remaining_amount',
        store=True,
        help="Remaining budget amount"
    )
    
    utilization_percentage = fields.Float(
        string='Utilization %',
        compute='_compute_utilization_percentage',
        help="Percentage of budget utilized"
    )
    
    currency_id = fields.Many2one(
        related='budget_id.currency_id',
        string='Currency',
        readonly=True
    )
    
    display_name = fields.Char(
        compute='_compute_display_name',
        string='Display Name',
        store=True
    )

    @api.depends('amount', 'utilized_amount')
    def _compute_remaining_amount(self):
        for record in self:
            record.remaining_amount = record.amount - record.utilized_amount

    @api.depends('amount', 'utilized_amount')
    def _compute_utilization_percentage(self):
        for record in self:
            if record.amount:
                record.utilization_percentage = (record.utilized_amount / record.amount) * 100
            else:
                record.utilization_percentage = 0.0

    @api.depends('budget_id', 'allocation_type', 'month')
    def _compute_display_name(self):
        for record in self:
            if record.budget_id and record.allocation_type and record.month:
                month_name = dict(record._fields['month'].selection)[record.month]
                record.display_name = f"{record.budget_id.name} - {record.allocation_type.title()} - {month_name}"
            else:
                record.display_name = "Budget Line"

    @api.constrains('amount')
    def _check_amount(self):
        for record in self:
            if record.amount < 0:
                raise ValidationError("Budget amount cannot be negative")

    @api.constrains('utilized_amount')
    def _check_utilized_amount(self):
        for record in self:
            if record.utilized_amount < 0:
                raise ValidationError("Utilized amount cannot be negative")
            if record.utilized_amount > record.amount:
                raise ValidationError("Utilized amount cannot exceed budget amount")

    def utilize_budget(self, amount, description=""):
        """Method to utilize budget amount"""
        for record in self:
            if amount > record.remaining_amount:
                raise ValidationError(
                    f"Cannot utilize {amount}. Only {record.remaining_amount} remaining."
                )
            record.utilized_amount += amount
            # Log the utilization - NOW THIS WILL WORK
            record.message_post(
                body=f"Budget utilized: {amount}. Description: {description}"
            )

    # Comment out these fields:
    # marketing_request_line_ids = fields.One2many(...)
    # total_requested_amount = fields.Float(...)
    # pending_request_amount = fields.Float(...)
    # approved_request_amount = fields.Float(...)
    # available_for_request = fields.Float(...)

    # Comment out these methods:
    # def _compute_total_requested_amount(self):
    # def _compute_pending_request_amount(self):
    # def _compute_approved_request_amount(self):
    # def _compute_available_for_request(self):