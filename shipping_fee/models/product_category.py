from odoo import api, fields, models, tools, SUPERUSER_ID, _
import logging
from datetime import date, datetime
from odoo.tools import format_amount

_logger = logging.getLogger(__name__)


class ProductCategory(models.Model):
    _inherit = "product.category"

    service_charges = fields.Float(string="Service Charges", store=True, tracking=True)


class PriceRule(models.Model):
    _inherit = "delivery.price.rule"

    categ_id = fields.Many2one('product.category', 'Category', store=True, required=True)

    @api.depends('variable', 'operator', 'max_value', 'list_base_price', 'list_price', 'variable_factor', 'currency_id','categ_id')
    def _compute_name(self):
        for rule in self:
            name = 'if %s %s %.02f then' % (rule.variable, rule.operator, rule.max_value)
            if rule.currency_id:
                base_price = format_amount(self.env, rule.list_base_price, rule.currency_id)
                price = format_amount(self.env, rule.list_price, rule.currency_id)
            else:
                base_price = "%.2f" % rule.list_base_price
                price = "%.2f" % rule.list_price
            if rule.list_base_price and not rule.list_price:
                name = '%s fixed price %s' % (name, base_price)
            elif rule.list_price and not rule.list_base_price:
                name = '%s %s times %s' % (name, price, rule.variable_factor)
            else:
                name = '%s fixed price %s plus %s times %s' % (
                    name, base_price, price, rule.variable_factor
                )
            if rule.categ_id:
                if rule.categ_id.parent_id:
                    if rule.categ_id.parent_id.parent_id:
                        name = f"{name} of {rule.categ_id.parent_id.parent_id.name} / {rule.categ_id.parent_id.name} / {rule.categ_id.name}"
                    else:
                        name = f"{name} of {rule.categ_id.parent_id.name} / {rule.categ_id.name}"
                else:
                    name = f"{name} of {rule.categ_id.name}"

            rule.name = name
