from odoo import api, fields, models, tools, SUPERUSER_ID
import logging
from datetime import date, datetime

_logger = logging.getLogger(__name__)


class ReasonCancel(models.Model):
    _name = "reason.cancel"
    _description = "Reason To Cancel"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'





    name = fields.Char(string="Reason", store=True, tracking=True)
