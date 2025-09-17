from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'New'),
        ('progress', 'In Progress'),
        ('return_accepted', 'Return Accepted'),
        ('ship', 'Ready To Ship'),
        ('assigned_to_picker', 'Assigned to Picker'),
        ('delivered', 'Shipped'),
        ('picked_from_customer', 'Picked from Customer'),
        ('done', 'Delivered'),
        ('cancel', 'Cancelled'),
    ], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=True, store=True, tracking=True,
        help=" * Draft: The transfer is not confirmed yet. Reservation doesn't apply.\n"
             " * Waiting another operation: This transfer is waiting for another operation before being ready.\n"
             " * Waiting: The transfer is waiting for the availability of some products.\n(a) The shipping policy is \"As soon as possible\": no product could be reserved.\n(b) The shipping policy is \"When all products are ready\": not all the products could be reserved.\n"
             " * Ready: The transfer is ready to be processed.\n(a) The shipping policy is \"As soon as possible\": at least one product has been reserved.\n(b) The shipping policy is \"When all products are ready\": all product have been reserved.\n"
             " * Done: The transfer has been processed.\n"
             " * Cancelled: The transfer has been cancelled.")

    cancel_reason_id = fields.Many2one('reason.cancel', string='Reason to Cancel', tracking=True)

    def action_in_progress(self):
        self.write({'state': 'progress'})

    def action_in_return_accepted(self):
        self.write({'state': 'return_accepted'})

    def action_in_assigned_to_picker(self):
        self.write({'state': 'assigned_to_picker'})

    def action_in_picked_from_customer(self):
        self.write({'state': 'picked_from_customer'})

    def action_ready_to_ship(self):
        self.write({'state': 'ship'})

    def action_delivered(self):
        self.write({'state': 'delivered'})

    def action_cancel(self):
        if not self.cancel_reason_id:
            raise ValidationError(_("Explain Reason to cancel"))
        self.move_ids._action_cancel()
        self.write({'is_locked': True})
        self.filtered(lambda x: not x.move_ids).state = 'cancel'
        return True


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    @api.depends('delivery_type')
    def _compute_can_generate_return(self):
        super(DeliveryCarrier, self)._compute_can_generate_return()
        for carrier in self:
            carrier.can_generate_return = True
