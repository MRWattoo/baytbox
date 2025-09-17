from odoo import api, fields, models, tools, SUPERUSER_ID, _
import logging
from datetime import date, datetime

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # shipping_charges = fields.Float(string="Shipping Charges", store=True, compute='shipping_fee')

    # @api.depends('order_line.product_id', 'order_line.product_template_id', 'order_line.product_uom_qty')
    # def shipping_fee(self):
    #     _logger.info("shipping_fee")
    #     _logger.info("Working")
    #     for rec in self:
    #         shipp_fee = 0
    #         if rec.state == 'draft':
    #             for line in rec.order_line:
    #                 if line.product_template_id and line.product_template_id.detailed_type != 'service':
    #                     _logger.info(line.product_template_id)
    #                     shipp_fee += line.product_uom_qty * line.product_template_id.categ_id.service_charges
    #
    #                 if line.product_template_id and line.product_template_id.detailed_type == 'service':
    #                     _logger.info(line.product_template_id)
    #                     line.price_unit = shipp_fee
    #
    #         rec.shipping_charges = shipp_fee


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    currency_id = fields.Many2one('res.currency', string="Currency",store=True,related="")

    def _get_price_available(self, order):
        _logger.info("OOOOOOOOOOOOOO")
        _logger.info("OOOOOOOOOOOOOO")
        _logger.info(order)
        self.ensure_one()
        price = 0.0
        price_rules = self.env['delivery.price.rule'].search([('carrier_id', '=', self.id)])
        _logger.info(price_rules)
        for line in order.order_line:
            product = line.product_template_id
            _logger.info(product)
            category = product.categ_id
            for rule in self.price_rule_ids:
                if rule.categ_id.id == category.id:
                    _logger.info("PPPPPPPsplitPPPPPPPP")
                    _logger.info(rule.id)

                    service_charges = rule.list_price
                    price += line.product_uom_qty * service_charges

            # for rule in price_rules.filtered(lambda r: r.categ_id.id == category.id):
            #     service_charges = rule.categ_id.service_charges
            #     price += line.product_uom_qty * service_charges
            #     _logger.info("jjdsjkgksdfjksgjklsdklglksldgkldshgklsdjklsdg")
            #     _logger.info("jjdsjkgksdfjksgjklsdklglksldgkldshgklsdjklsdg")
            #     _logger.info(price)

            # delivery_rule = self.price_rule_ids.filtered(lambda r: r.categ_id.id == category.id)
            # _logger.info("KKKKKKKKKKKKKKKKKKK")
            # _logger.info(delivery_rule)
            #
            # if delivery_rule:
            #     service_charges = category.service_charges
            #     price += line.product_uom_qty * service_charges

            # price_rules = self.env['delivery.price.rule'].search([('carrier_id', '=', self.id)])
            # for rule in price_rules:
            #     _logger.info("Delivery Rule: %s, Category: %s", rule, rule.categ_id)

        return price
    def _get_conversion_currencies(self, order, conversion):
        # if conversion == 'company_to_pricelist':
        #     from_currency, to_currency = order.company_id.currency_id, order.currency_id
        # elif conversion == 'pricelist_to_company':
        #     from_currency, to_currency = order.currency_id, order.company_id.currency_id
        from_currency = order.currency_id
        to_currency = order.currency_id
        return from_currency, to_currency
