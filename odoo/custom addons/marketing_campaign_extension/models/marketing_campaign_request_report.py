from odoo import models, fields, api

class MarketingCampaignRequestReport(models.Model):
    _name = 'marketing.campaign.request.report'
    _description = 'Marketing Campaign Request Report'
    _auto = False

    campaign_id = fields.Many2one('marketing.campaign', string='Campaign')
    campaign_name = fields.Char(string='Campaign Name')
    campaign_start_date = fields.Datetime(string='Start Date')
    campaign_end_date = fields.Datetime(string='End Date')
    campaign_status = fields.Selection([
        ('draft', 'New'),
        ('running', 'Running'),
        ('stopped', 'Stopped')
    ], string='Campaign Status')
    request_id = fields.Many2one('marketing.request', string='Request')
    request_name = fields.Char(string='Request Name')
    unit_name = fields.Char(string='Unit Name')
    requestor_name = fields.Char(string='Requestor Name')
    request_type = fields.Char(string='Request Type')

    def init(self):
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW marketing_campaign_request_report AS (
                SELECT
                    row_number() OVER() AS id,
                    c.id AS campaign_id,
                    utm.name AS campaign_name,
                    NULL AS campaign_start_date,
                    NULL AS campaign_end_date,
                    c.state AS campaign_status,
                    r.id AS request_id,
                    r.name AS request_name,
                    co.name AS unit_name,
                    r.requestor_name AS requestor_name,
                    r.request_type AS request_type
                FROM marketing_campaign_request_rel rel
                JOIN marketing_campaign c ON rel.campaign_id = c.id
                JOIN utm_campaign utm ON c.utm_campaign_id = utm.id
                JOIN marketing_request r ON rel.request_id = r.id
                LEFT JOIN res_company co ON r.unit = co.id
            )
        ''')
