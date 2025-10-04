# -*- coding: utf-8 -*-
#################################################################################
# Author : Your Company
# Copyright(c): 2025-Present Your Company
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#################################################################################

from odoo import models, fields, api, _
import logging
from datetime import datetime
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class UnitBudget(models.Model):
    _name = 'unit.budget'
    _description = "Unit Budget"
    _rec_name = 'name'
    _order = 'year desc, unit_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string="Budget Code", 
        required=True, 
        copy=False, 
        readonly=True, 
        default='New',
        help="Auto-generated budget code"
    )
    
    unit_id = fields.Many2one(
        'res.company',
        string="Unit", 
        required=True,
        help="Business unit for this budget",
        tracking=True
    )
    
    year = fields.Integer(
        string="Budget Year", 
        required=True,
        default=lambda self: datetime.now().year,
        help="Fiscal year for this budget",
        tracking=True
    )
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        required=True
    )
    
    total_budget = fields.Float(
        string="Total Budget Amount",
        compute='_compute_total_budget',
        store=True,
        help="Total budget allocated for this unit and year",
        tracking=True
    )
    
    budget_utilization = fields.Float(
        string="Budget Utilization",
        compute='_compute_budget_utilization',
        help="Amount of budget already utilized"
    )
    
    remaining_budget = fields.Float(
        string="Remaining Budget",
        compute='_compute_remaining_budget',
        help="Remaining budget amount"
    )
    
    utilization_percentage = fields.Float(
        string="Utilization %",
        compute='_compute_utilization_percentage',
        help="Percentage of budget utilized"
    )
    
    notes = fields.Text(string="Notes")
    
    budget_line_ids = fields.One2many(
        'unit.budget.line',
        'budget_id',
        string="Budget Lines",
        help="Detailed budget allocation by type and month"
    )
    
    store_promotion_budget = fields.Float(
        string="Store Promotion Budget",
        compute='_compute_allocation_budgets',
        help="Total budget for store promotion"
    )
    
    product_promotion_budget = fields.Float(
        string="Product Promotion Budget",
        compute='_compute_allocation_budgets',
        help="Total budget for product promotion"
    )
    
    influencer_promotion_budget = fields.Float(
        string="Influencer Promotion Budget",
        compute='_compute_allocation_budgets',
        help="Total budget for influencer promotion"
    )

    # ADD BACK: Marketing request summary
    # marketing_request_summary_ids = fields.One2many(
    #     'marketing.request.budget.line',
    #     'budget_id',
    #     string='Marketing Request Summary',
    #     help="All marketing request lines for this budget"
    # )
    
    # total_marketing_requests = fields.Float(
    #     string='Total Marketing Requests',
    #     compute='_compute_marketing_request_totals',
    #     store=True,
    #     help="Total amount requested through marketing requests"
    # )
    
    # pending_marketing_requests = fields.Float(
    #     string='Pending Marketing Requests',
    #     compute='_compute_marketing_request_totals',
    #     store=True,
    #     help="Total pending marketing request amount"
    # )
    
    # approved_marketing_requests = fields.Float(
    #     string='Approved Marketing Requests',
    #     compute='_compute_marketing_request_totals',
    #     store=True,
    #     help="Total approved marketing request amount"
    # )

    # Compute methods
    @api.depends('budget_line_ids.amount')
    def _compute_total_budget(self):
        for record in self:
            record.total_budget = sum(record.budget_line_ids.mapped('amount'))
    
    @api.depends('budget_line_ids.utilized_amount')
    def _compute_budget_utilization(self):
        for record in self:
            record.budget_utilization = sum(record.budget_line_ids.mapped('utilized_amount'))
    
    @api.depends('total_budget', 'budget_utilization')
    def _compute_remaining_budget(self):
        for record in self:
            record.remaining_budget = record.total_budget - record.budget_utilization
    
    @api.depends('total_budget', 'budget_utilization')
    def _compute_utilization_percentage(self):
        for record in self:
            if record.total_budget:
                record.utilization_percentage = (record.budget_utilization / record.total_budget) * 100
            else:
                record.utilization_percentage = 0.0
    
    @api.depends('budget_line_ids.amount', 'budget_line_ids.allocation_type')
    def _compute_allocation_budgets(self):
        for record in self:
            store_lines = record.budget_line_ids.filtered(lambda l: l.allocation_type == 'store')
            product_lines = record.budget_line_ids.filtered(lambda l: l.allocation_type == 'product')
            influencer_lines = record.budget_line_ids.filtered(lambda l: l.allocation_type == 'influencer')
            
            record.store_promotion_budget = sum(store_lines.mapped('amount'))
            record.product_promotion_budget = sum(product_lines.mapped('amount'))
            record.influencer_promotion_budget = sum(influencer_lines.mapped('amount'))

    # @api.depends('marketing_request_summary_ids.requested_amount', 'marketing_request_summary_ids.marketing_request_id.approval_status')
    # def _compute_marketing_request_totals(self):
    #     for record in self:
    #         # Check if the marketing.request.budget.line model exists
    #         if 'marketing.request.budget.line' not in self.env:
    #             record.total_marketing_requests = 0.0
    #             record.pending_marketing_requests = 0.0
    #             record.approved_marketing_requests = 0.0
    #             continue
                
    #         all_lines = record.marketing_request_summary_ids
    #         pending_lines = all_lines.filtered(
    #             lambda l: l.marketing_request_id.approval_status in ['draft', 'submitted']
    #         )
    #         approved_lines = all_lines.filtered(
    #             lambda l: l.marketing_request_id.approval_status == 'approved'
    #         )
            
    #         record.total_marketing_requests = sum(all_lines.mapped('requested_amount'))
    #         record.pending_marketing_requests = sum(pending_lines.mapped('requested_amount'))
    #         record.approved_marketing_requests = sum(approved_lines.mapped('requested_amount'))

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('unit.budget') or 'New'
        return super(UnitBudget, self).create(vals)
    
    @api.constrains('year')
    def _check_year(self):
        for record in self:
            current_year = datetime.now().year
            if record.year < 2000 or record.year > current_year + 10:
                raise ValidationError(_("Please enter a valid year between 2000 and %s") % (current_year + 10))
    
    @api.constrains('unit_id', 'year')
    def _check_unique_unit_year(self):
        for record in self:
            existing = self.search([
                ('unit_id', '=', record.unit_id.id),
                ('year', '=', record.year),
                ('id', '!=', record.id)
            ])
            if existing:
                raise ValidationError(_("A budget already exists for unit '%s' in year %s") % 
                                    (record.unit_id.name, record.year))
    
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.name} - {record.unit_id.name} ({record.year})"
            result.append((record.id, name))
        return result
    
    def action_confirm(self):
        for record in self:
            if record.state != 'draft':
                raise UserError(_("Only draft budgets can be confirmed"))
            record.state = 'confirmed'
    
    def action_approve(self):
        for record in self:
            if record.state != 'confirmed':
                raise UserError(_("Only confirmed budgets can be approved"))
            record.state = 'approved'
    
    def action_cancel(self):
        for record in self:
            if record.state == 'approved':
                raise UserError(_("Cannot cancel an approved budget"))
            record.state = 'cancelled'
    
    def action_reset_to_draft(self):
        for record in self:
            record.state = 'draft'

    # ADD BACK: Action method
    # def action_view_marketing_requests(self):
    #     """Open marketing requests for this budget"""
    #     return {
    #         'name': 'Marketing Requests',
    #         'view_mode': 'list,form',
    #         'res_model': 'marketing.request',
    #         'type': 'ir.actions.act_window',
    #         'domain': [('unit_budget_id', '=', self.id)],
    #         'context': {'default_unit_budget_id': self.id}
    #     }