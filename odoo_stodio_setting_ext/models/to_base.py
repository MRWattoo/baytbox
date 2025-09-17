import logging

from odoo import models, fields, _


_logger = logging.getLogger(__name__)


class Contacts(models.Model):
    _inherit = "res.partner"

    x_studio_phone_2 = fields.Char(name="Phone 2")
    x_studio_social_media = fields.Char(name="Social Media")

# class PurchaseOrder(models.Model):
#     _inherit = "purchase.order"
#
#     x_studio_phone_2 = fields.Integer(name="New Integer")


class ProductPriceListItem(models.Model):
    _inherit = "product.pricelist.item"

    x_studio_product_category = fields.Many2one('product.category',related="product_tmpl_id.categ_id",name="Product Category")
    x_studio_product_variant_category = fields.Many2one('product.category',related="product_id.categ_id", name="Product Variant Category")


