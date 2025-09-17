from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def get_active_attribute_values(self):
        published_products = self.search([('is_published', '=', True)])
        active_values = published_products.mapped('attribute_line_ids.value_ids')
        return active_values
