from odoo import api, fields, models
from odoo.exceptions import ValidationError

class MarketingRequest(models.Model):
    _name = 'marketing.request'
    _description = 'Marketing Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Request ID', required=True, copy=False, readonly=True, default='New')
    requestor_name = fields.Char(string='Requestor Name', required=True, default=lambda self: self.env.user.partner_id.name)
    department = fields.Many2one('hr.department', string='Department', default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1).department_id.id)
    unit = fields.Many2one('res.company', string='Unit')
    
    # Add the Many2one relation to unit_budget with domain
    allocated_budget = fields.Many2one(
        'unit.budget',
        string='Allocated Budget',
        help="Select the unit budget for this marketing request",
        tracking=True
    )

    request_type = fields.Selection([
        ('design', 'Design'),
        ('promotion', 'Promotion'),
        ('campaign', 'Campaign'),
        ('other', 'Other')
    ], string='Request Type', required=True)
    
    priority = fields.Selection([
        ('1', 'Low'),
        ('2', 'Medium'),
        ('3', 'High')
    ], string='Priority', default='3')
    
    category = fields.Selection([
        ('tiles', 'Tiles'),
        ('sanitary', 'Sanitary'),
        ('other', 'Other')
    ], string='Category', required=True)
    
    product_ids = fields.Many2many('product.template', 'marketing_request_product_rel',
                                'request_id', 'product_id', string='Products')
    product_description = fields.Text(string='Product Description')
    budget = fields.Float(string='Budget (INR)')
    deadline = fields.Datetime(string='Deadline')
    storepromotion = fields.Float(string='Store Promotion AMT(INR)')
    productpromotion = fields.Float(string='Product Promotion AMT(INR)')
    influencerpromotion = fields.Float(string='Influencer Promotion AMT(INR)')

    stage = fields.Selection([
        ('request', 'Request'),
        ('approved', 'Approved'),
        ('canceled', 'Canceled')
    ], string='Stage', default='request', tracking=True)

    approval_status = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Approval Status', default='draft', tracking=True)
    
    approved_by = fields.Many2one('res.users', string='Approved By', readonly=True)
    completion_status = fields.Selection([
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Completion Status', default='not_started', tracking=True)

    # Add these fields to your existing MarketingRequest class
    budget_amount = fields.Float('Budget Amount')
    allocation_type = fields.Selection([
        ('product', 'Product Promotion'),
        ('store', 'Store Promotion'),
        ('influencer', 'Influencer Promotion')
    ], string='Allocation Type')

    campaign_ids = fields.Many2many(
        'marketing.campaign',
        'marketing_campaign_request_rel',
        'request_id',
        'campaign_id',
        string='Campaigns',
    )

    unit_budget_line_ids = fields.Many2many(
        'unit.budget.line',
        'marketing_request_budget_line_rel',
        'marketing_request_id',
        'unit_budget_line_id',
        string='Budget Lines',
        help="Budget lines associated with the selected unit budget"
    )

    budget_line_amount_ids = fields.One2many(
        'marketing.request.budget.line.amount',
        'marketing_request_id',
        string='Budget Line Amounts'
    )

    # Add onchange method to filter allocated_budget based on selected unit
    @api.onchange('unit')
    def _onchange_unit(self):
        """Filter allocated budget based on selected unit"""
        if self.unit:
            # Clear the allocated_budget when unit changes
            self.allocated_budget = False
            # Return domain to filter unit budgets by selected unit
            return {
                'domain': {
                    'allocated_budget': [('unit_id', '=', self.unit.id)]
                }
            }
        else:
            # If no unit selected, clear allocated_budget and show no options
            self.allocated_budget = False
            return {
                'domain': {
                    'allocated_budget': [('id', '=', False)]
                }
            }

    @api.onchange('allocated_budget')
    def _onchange_allocated_budget(self):
        """Filter budget lines based on selected allocated budget"""
        if self.allocated_budget:
            # Clear existing selections when allocated budget changes
            self.unit_budget_line_ids = [(5, 0, 0)]  # Clear all
            # Return domain to filter budget lines by selected allocated budget
            return {
                'domain': {
                    'unit_budget_line_ids': [('unit_budget_id', '=', self.allocated_budget.id)]
                }
            }
        else:
            # If no allocated budget selected, clear budget lines and show no options
            self.unit_budget_line_ids = [(5, 0, 0)]
            return {
                'domain': {
                    'unit_budget_line_ids': [('id', '=', False)]
                }
            }

    @api.onchange('unit_budget_line_ids')
    def _onchange_unit_budget_line_ids(self):
        """Auto-create budget line amount records when budget lines are selected"""
        if self.unit_budget_line_ids:
            # Get existing budget line amount records
            existing_lines = {line.unit_budget_line_id.id: line for line in self.budget_line_amount_ids}
            
            # Create new budget line amount records for newly selected lines
            new_records = []
            for budget_line in self.unit_budget_line_ids:
                if budget_line.id not in existing_lines:
                    new_records.append((0, 0, {
                        'unit_budget_line_id': budget_line.id,
                        'requested_amount': 0.0,
                    }))
            
            # Remove records for unselected budget lines
            records_to_remove = []
            for line in self.budget_line_amount_ids:
                if line.unit_budget_line_id.id not in self.unit_budget_line_ids.ids:
                    records_to_remove.append((2, line.id))
            
            # Update the budget_line_amount_ids field
            if new_records or records_to_remove:
                self.budget_line_amount_ids = new_records + records_to_remove
        else:
            # If no budget lines selected, clear all amount records
            self.budget_line_amount_ids = [(5, 0, 0)]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('marketing.request') or 'New'
        return super().create(vals_list)

    def action_submit(self):
        for rec in self:
            rec.approval_status = 'submitted'

    def action_approve(self):
        """Add budget validation to approval process"""
        for record in self:
            if record.budget_amount and record.allocation_type:
                # Get unit name
                unit_id = record.unit
                unit_record = self.env['res.company'].browse(unit_id) if isinstance(unit_id, int) else unit_id
                unit_name = unit_record.name if unit_record and hasattr(unit_record, 'name') else ''
                
                # Check budget availability
                budget_allocation = self.env['budget.allocation']
                budget_allocation.check_budget_availability(
                    unit_name=unit_name,
                    category=record.category,
                    request_type=record.request_type,
                    allocation_type=record.allocation_type,
                    amount=record.budget_amount
                )
                
                # If check passes, utilize the budget
                budget_allocation.utilize_budget(
                    unit_name=unit_name,
                    category=record.category,
                    request_type=record.request_type,
                    allocation_type=record.allocation_type,
                    amount=record.budget_amount,
                    marketing_request_id=record.id,
                    description=f"Budget utilization for marketing request: {record.name}"
                )
        
        # Continue with normal approval process
        self.write({'stage': 'approved'})

    def action_cancel(self):
        for rec in self:
            rec.approval_status = 'rejected'

    @api.constrains('budget_amount')
    def _check_budget_amount(self):
        """Validate budget amount when creating/updating marketing requests"""
        for record in self:
            if record.budget_amount and record.allocation_type and record.stage == 'draft':
                # Get unit name
                unit_id = record.unit
                unit_record = self.env['res.company'].browse(unit_id) if isinstance(unit_id, int) else unit_id
                unit_name = unit_record.name if unit_record and hasattr(unit_record, 'name') else ''
                
                # Check budget availability (this will raise error if insufficient)
                budget_allocation = self.env['budget.allocation']
                try:
                    budget_allocation.check_budget_availability(
                        unit_name=unit_name,
                        category=record.category,
                        request_type=record.request_type,
                        allocation_type=record.allocation_type,
                        amount=record.budget_amount
                    )
                except ValidationError as e:
                    raise ValidationError(f"Budget validation failed: {str(e)}")

    @api.constrains('allocated_budget', 'unit')
    def _check_allocated_budget_unit(self):
        """Ensure allocated budget belongs to the selected unit"""
        for record in self:
            if record.allocated_budget and record.unit:
                if record.allocated_budget.unit_id != record.unit:
                    raise ValidationError(
                        f"The selected budget '{record.allocated_budget.name}' does not belong to "
                        f"the selected unit '{record.unit.name}'. Please select a budget that "
                        f"belongs to the chosen unit."
                    )

    def action_reset_to_draft(self):
        """Reset marketing request back to draft status"""
        for record in self:
            record.write({
                'approval_status': 'draft',
                'stage': 'request',
                'approved_by': False
            })


# Create a new model for the request amounts per budget line
class MarketingRequestBudgetLineAmount(models.Model):
    _name = 'marketing.request.budget.line.amount'
    _description = 'Marketing Request Budget Line Amount'
    _rec_name = 'display_name'

    marketing_request_id = fields.Many2one(
        'marketing.request',
        string='Marketing Request',
        required=True,
        ondelete='cascade'
    )
    
    unit_budget_line_id = fields.Many2one(
        'unit.budget.line',
        string='Budget Line',
        required=True
    )
    
    requested_amount = fields.Float(
        string='Requested Amount',
        required=True,
        default=0.0
    )
    
    # Use Selection field to match unit.budget.line.allocation_type
    allocation_type = fields.Selection([
        ('store', 'Store Promotion'),
        ('product', 'Product Promotion'),
        ('influencer', 'Influencer Promotion')
    ], string='Allocation Type', related='unit_budget_line_id.allocation_type', readonly=True)
    
    # Use Selection field to match unit.budget.line.month
    month = fields.Selection([
        ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
        ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
        ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ], string='Month', related='unit_budget_line_id.month', readonly=True)
    
    allocated_amount = fields.Float(
        string='Allocated Amount',
        related='unit_budget_line_id.amount',
        readonly=True
    )
    
    utilized_amount = fields.Float(
        string='Utilized Amount',
        related='unit_budget_line_id.utilized_amount',
        readonly=True
    )
    
    available_amount = fields.Float(
        string='Available Amount',
        compute='_compute_available_amount',
        readonly=True
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        related='unit_budget_line_id.currency_id',
        readonly=True
    )
    
    display_name = fields.Char(
        compute='_compute_display_name',
        string='Display Name'
    )

    @api.depends('unit_budget_line_id.amount', 'unit_budget_line_id.utilized_amount')
    def _compute_available_amount(self):
        for record in self:
            record.available_amount = record.allocated_amount - record.utilized_amount

    @api.depends('unit_budget_line_id', 'requested_amount')
    def _compute_display_name(self):
        for record in self:
            if record.unit_budget_line_id:
                record.display_name = f"{record.unit_budget_line_id.display_name} - Requested: {record.requested_amount}"
            else:
                record.display_name = f"Requested: {record.requested_amount}"

    @api.constrains('requested_amount', 'available_amount')
    def _check_requested_amount(self):
        for record in self:
            if record.requested_amount > record.available_amount:
                raise ValidationError(
                    f"Requested amount ({record.requested_amount}) cannot exceed "
                    f"available amount ({record.available_amount}) for budget line "
                    f"{record.unit_budget_line_id.display_name}"
                )


