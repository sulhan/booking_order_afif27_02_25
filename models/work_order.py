from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime

class WorkOrder(models.Model):
    _name = 'work.order'
    _description = 'Work Order'

    name = fields.Char(string='WO Number', required=True, readonly=True, copy=False, default=lambda self: self.env['ir.sequence'].next_by_code('work.order'))
    booking_order_id = fields.Many2one('sale.order', string='Booking Order Reference', readonly=True)
    team_id = fields.Many2one('service.team', string='Team', required=True)
    team_leader = fields.Many2one('res.users', string='Team Leader', required=True)
    team_members = fields.Many2many('res.users', string='Team Members')
    planned_start = fields.Datetime(string='Planned Start', required=True)
    planned_end = fields.Datetime(string='Planned End', required=True)
    date_start = fields.Datetime(string='Date Start', readonly=True)
    date_end = fields.Datetime(string='Date End', readonly=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='State', default='pending')
    notes = fields.Text(string='Notes')
    
    	 # Action untuk memulai pekerjaan
    def action_start_work_order(self):
        for record in self:
            record.write({
                'state': 'in_progress',
                'date_start': datetime.now(),
            })

    # Action untuk menyelesaikan pekerjaan
    def action_end_work_order(self):
        for record in self:
            if record.state != 'in_progress':
                raise UserError("Work Order must be in progress before it can be completed.")
            record.write({
                'state': 'done',
                'date_end': datetime.now(),
            })

    # Action untuk reset ke pending
    def action_reset_work_order(self):
        for record in self:
            if record.state != 'in_progress':
                raise UserError("Only Work Orders in progress can be reset.")
            record.write({
                'state': 'pending',
                'date_start': False,
            })

    # Action untuk membatalkan pekerjaan
    def action_cancel_work_order(self):
        for record in self:
            if not record.cancel_reason:
                raise UserError("You must provide a reason for cancellation.")
            record.write({
                'state': 'cancelled',
                'notes': (record.notes or '') + "\nCancellation Reason: " + record.cancel_reason,
            })



class WorkOrderReport(models.AbstractModel):
    _name = 'report.booking_order_afif27_02_25.report_work_order'
    _description = 'Work Order Report'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('booking_order_afif27_02_25.report_work_order')
        docs = self.env['work.order'].browse(docids)
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': docs,
        }
        return report_obj.render('booking_order_afif27_02_25.report_work_order', docargs)


