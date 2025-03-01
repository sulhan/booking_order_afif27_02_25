from odoo import models, fields
from odoo.exceptions import UserError


class BookingOrder(models.Model):
    _name = 'booking.order'  # Menggunakan nama unik
    _description = 'Booking Order'
    
    is_booking_order = fields.Boolean(string="Is Booking Order", default=True)
    team_id = fields.Many2one('service.team', string='Team', required=True)
    team_leader = fields.Many2one('res.users', string='Team Leader', required=True)
    team_members = fields.Many2many('res.users', string='Team Members')
    booking_start = fields.Datetime(string='Booking Start', required=True)
    booking_end = fields.Datetime(string='Booking End', required=True)
    
    def action_check_availability(self):
        for record in self:
            overlap = self.env['work.order'].search([
                ('team_id', '=', record.team_id.id),
                ('state', '!=', 'cancelled'),
                ('planned_start', '<', record.booking_end),
                ('planned_end', '>', record.booking_start),
            ])
            if overlap:
                raise UserError("Team already has work order during that period on {overlap[0].booking_order_reference_id.name}")
            else:
                raise UserError("Team is available for booking")
    def action_confirm(self):
        for record in self:
            if record.is_booking_order:
                overlap = self.env['work.order'].search([
                    ('team_id', '=', record.team_id.id),
                    ('state', '!=', 'cancelled'),
                    ('planned_start', '<', record.booking_end),
                    ('planned_end', '>', record.booking_start),
                ])
                if overlap:
                    raise UserError("Team is not available during this period, already booked on {overlap[0].booking_order_reference_id.name}. Please book on another date.")
                else:
                    work_order = self.env['work.order'].create({
                        'booking_order_reference_id': record.id,
                        'team_id': record.team_id.id,
                        'team_leader_id': record.team_leader_id.id,
                        'team_member_ids': [(6, 0, record.team_member_ids.ids)],
                        'planned_start': record.booking_start,
                        'planned_end': record.booking_end,
                        'state': 'pending',
                    })
                    record.write({'work_order_id': work_order.id})
        return super(SaleOrder, self).action_confirm()
