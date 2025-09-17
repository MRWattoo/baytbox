# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = "product.product"

    saler_sku = fields.Char(string="SKU")
    def _get_discount_price_wss(self):
        template = self
        compare_list_price_low = compare_list_price = self.env['product.pricelist.item'].search(
            [('product_id', '=', template.id)], limit=1, order="compare_list_price asc").compare_list_price
        price_reduce = price_reduce2 = self.env['product.pricelist.item'].search(
            [('product_id', '=', template.id)], limit=1, order="fixed_price asc").fixed_price
        if not compare_list_price and not price_reduce:
            compare_list_price_low = compare_list_price = self.env['product.pricelist.item'].search(
                [('product_tmpl_id', '=', template.product_tmpl_id.id)], limit=1, order="compare_list_price asc").compare_list_price
            price_reduce = price_reduce2 = self.env['product.pricelist.item'].search(
                [('product_tmpl_id', '=', template.product_tmpl_id.id)], limit=1, order="fixed_price asc").fixed_price

        if template._name == 'product.template':
            product_ids = self.env['product.product'].sudo().search([('product_tmpl_id', '=', template.id)])
            for product_id in product_ids:
                price_list = self.env['product.pricelist.item'].search([('product_id', '=', product_id.id)], limit=1,
                                                                       order="id desc")
                price_reduce_check = price_list.fixed_price
                compare_list_price_check = price_list.compare_list_price
                if compare_list_price_low > compare_list_price_check:
                    compare_list_price_low = compare_list_price_check
                if compare_list_price < compare_list_price_check:
                    compare_list_price = compare_list_price_check
                if price_reduce > price_reduce_check:
                    price_reduce = price_reduce_check
                if price_reduce2 < price_reduce_check:
                    price_reduce2 = price_reduce_check
        base_percent = base_percent2 = 0
        delivery_lead_time = template.product_tmpl_id.sale_delay
        delivery_lead_time2 = 1
        if delivery_lead_time > 3:
            delivery_lead_time2 = delivery_lead_time - 3
        if price_reduce2 == price_reduce:
            price_reduce2 = False
        if compare_list_price != 0 and price_reduce2 != 0:
            base_percent2 = 100 - (price_reduce2 * 100 / compare_list_price)
        if compare_list_price_low != 0 and price_reduce != 0:
            base_percent = 100 - (price_reduce * 100 / compare_list_price_low)

        template_price_vals = {
            'base_percent2': int(round(base_percent2, 0)),
            'base_percent': int(round(base_percent, 0)),
            'delivery_lead_time': delivery_lead_time,
            'delivery_lead_time2': delivery_lead_time2,
        }

        return template_price_vals

class ProductPriceList(models.Model):
    _inherit = "product.pricelist.item"

    compare_list_price = fields.Monetary(
        string="Compare to Price",
        help="The amount will be displayed strikethroughed on the eCommerce product page")
    delivery_fee = fields.Monetary(
        string="Delivery Fee",
        help="The amount will be displayed strikethroughed on the eCommerce product page")

class ProductTemplate(models.Model):
    _inherit = "product.template"


    truncated_name = fields.Char(compute='_compute_truncated_name', string='Truncated Name')

    def get_alter_products(self):
        products = []
        if self.categ_id.id == 7:
            products+=self.env['product.template'].search([('categ_id','=',44),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',9),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
        if self.categ_id.id == 50:
            products+=self.env['product.template'].search([('categ_id','=',10),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',47),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
        if self.categ_id.id == 44:
            products+=self.env['product.template'].search([('categ_id','=',5),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',11),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
        if self.categ_id.id == 9:
            products+=self.env['product.template'].search([('categ_id','=',5),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',11),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
        if self.categ_id.id == 13:
            products+=self.env['product.template'].search([('categ_id','=',5),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',11),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
        if self.categ_id.id == 43:
            products+=self.env['product.template'].search([('categ_id','=',42),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',48),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
        if self.categ_id.id == 42:
            products+=self.env['product.template'].search([('categ_id','=',43),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',48),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
        if self.categ_id.id == 48:
            products+=self.env['product.template'].search([('categ_id','=',43),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',42),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
        if self.categ_id.id == 10:
            products+=self.env['product.template'].search([('categ_id','=',50),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',5),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
        if self.categ_id.id == 41:
            products+=self.env['product.template'].search([('categ_id','=',47),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',49),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
        if self.categ_id.id == 47:
            products+=self.env['product.template'].search([('categ_id','=',5),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',50),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',7),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',11),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
        if self.categ_id.id == 49:
            products+=self.env['product.template'].search([('categ_id','=',47),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',44),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
        if self.categ_id.id == 11:
            products+=self.env['product.template'].search([('categ_id','=',8),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',9),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',13),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',44),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
        if self.categ_id.id == 46:
            products+=self.env['product.template'].search([('categ_id','=',48),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',40),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',29),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
        if self.categ_id.id == 29:
            products+=self.env['product.template'].search([('categ_id','=',46),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',48),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',40),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
        if self.categ_id.id == 5:
            products+=self.env['product.template'].search([('categ_id','=',44),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',9),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
            products+=self.env['product.template'].search([('categ_id','=',13),('is_published','=',True),('website_id','=',self.website_id.id)],limit=4).ids
        _logger.info(self.categ_id.id)
        _logger.info(products)
        self.write({'alternative_product_ids': products})
    # def get_alter_products_beds(self):
    #     self.alternative_product_ids = self.env['product.template'].search([('categ_id','in',[10,47])]).ids

    def _compute_truncated_name(self):
        for product in self:
            if len(product.name)>40:
                product.truncated_name = (product.name[:40] + '...') if len(product.name) > 40 else product.name
            else:
                product.truncated_name = (f"{product.name}                               ...")

    def _get_additional_combination_info(self, product_or_template, quantity, date, website):
        combination_info = super(ProductTemplate,self)._get_additional_combination_info(product_or_template, quantity, date, website)
        compare_list_price = self.env['product.pricelist.item'].search([('product_id','=',product_or_template.id)],limit=1,order="compare_list_price desc").compare_list_price
        if compare_list_price == 0:
            compare_list_price = self.env['product.pricelist.item'].search([('product_tmpl_id','=',product_or_template.id),('compare_list_price','!=',0)],limit=1,order="compare_list_price desc").compare_list_price
        if compare_list_price == 0 and product_or_template._name == 'product.product':
            compare_list_price = self.env['product.pricelist.item'].search([('product_tmpl_id','=',product_or_template.product_tmpl_id.id),('compare_list_price','!=',0)],limit=1,order="compare_list_price desc").compare_list_price
        compare_list_price = product_or_template.currency_id._convert(
            from_amount=compare_list_price,
            to_currency=self.currency_id,
            company=self.env.company,
            date=date,
            round=False)
        compare_list_price_low = compare_list_price = None
        price_reduce = price_reduce2 = None
        if product_or_template._name == 'product.product':
            compare_list_price_low = compare_list_price = self.env['product.pricelist.item'].search(
                [('product_id', '=', product_or_template.id)], limit=1, order="compare_list_price asc").compare_list_price
            price_reduce = price_reduce2 = self.env['product.pricelist.item'].search(
                [('product_id', '=', product_or_template.id)], limit=1, order="fixed_price asc").fixed_price
        template = product_or_template
        if template._name == 'product.template':
            if not compare_list_price and not price_reduce:
                compare_list_price_low = compare_list_price = self.env['product.pricelist.item'].search(
                    [('product_tmpl_id', '=', product_or_template.id)],
                    limit=1, order="compare_list_price asc").compare_list_price
                price_reduce = price_reduce2 = self.env['product.pricelist.item'].search(
                    [('product_tmpl_id', '=', product_or_template.id)], limit=1,
                    order="fixed_price asc").fixed_price

            product_ids = self.env['product.product'].sudo().search([('product_tmpl_id', '=', product_or_template.id)])
            for product_id in product_ids:
                price_list = self.env['product.pricelist.item'].search([('product_id', '=', product_or_template.id)], limit=1,
                                                                       order="id desc")
                price_reduce_check = price_list.fixed_price
                compare_list_price_check = price_list.compare_list_price
                if compare_list_price_low > compare_list_price_check:
                    compare_list_price_low = compare_list_price_check
                if compare_list_price < compare_list_price_check:
                    compare_list_price = compare_list_price_check
                if price_reduce > price_reduce_check:
                    price_reduce = price_reduce_check
                if price_reduce2 < price_reduce_check:
                    price_reduce2 = price_reduce_check
        base_percent = base_percent2 = 0
        delivery_lead_time = template.sale_delay
        delivery_lead_time2 = 1
        if delivery_lead_time > 3:
            delivery_lead_time2 = delivery_lead_time - 3
        if price_reduce2 == price_reduce:
            price_reduce2 = False
        if compare_list_price != 0 and price_reduce2 != 0:
            base_percent2 = 100 - (price_reduce2 * 100 / compare_list_price)
        if compare_list_price_low != 0 and price_reduce != 0:
            base_percent = 100 - (price_reduce * 100 / compare_list_price_low)

        template_price_vals = {
            'base_percent2': int(round(base_percent2, 0)),
            'base_percent': int(round(base_percent, 0)),
            'delivery_lead_time': int(delivery_lead_time),
            'delivery_lead_time2': int(delivery_lead_time2),
        }

        combination_info['compare_list_price'] = compare_list_price
        combination_info['price'] = compare_list_price
        combination_info['base_percent2'] = int(round(base_percent2,2))
        combination_info['base_percent'] = int(round(base_percent,2))
        combination_info['delivery_lead_time'] = int(delivery_lead_time)
        combination_info['delivery_lead_time2'] = int(delivery_lead_time2)
        return combination_info

    def _get_sales_prices(self, pricelist, fiscal_position):
        super(ProductTemplate,self)._get_sales_prices( pricelist, fiscal_position)
        if not self:
            return {}

        pricelist and pricelist.ensure_one()
        partner_sudo = self.env.user.partner_id
        pricelist = pricelist or self.env['product.pricelist']
        currency = pricelist.currency_id or self.env.company.currency_id
        date = fields.Date.context_today(self)

        sales_prices = pricelist._get_products_price(self, 1.0)
        show_discount = pricelist and pricelist.discount_policy == 'without_discount'

        base_sales_prices = self._price_compute('list_price', currency=currency)
        website = self.env['website'].get_current_website()
        if website.show_line_subtotals_tax_selection == 'tax_excluded':
            tax_display = 'total_excluded'
        else:
            tax_display = 'total_included'

        res = {}
        for template in self:

            price_reduce = sales_prices[template.id]

            product_taxes = template.sudo().taxes_id.filtered(lambda t: t.company_id == t.env.company)
            taxes = fiscal_position.map_tax(product_taxes)

            base_price = None
            price_list_contains_template = currency.compare_amounts(price_reduce, base_sales_prices[template.id]) != 0

            if template.compare_list_price:
                base_price = template.compare_list_price
                if not price_list_contains_template:
                    price_reduce = base_sales_prices[template.id]

                if template.currency_id != pricelist.currency_id:
                    base_price = template.currency_id._convert(
                        base_price,
                        pricelist.currency_id,
                        self.env.company,
                        date,
                        round=False
                    )

            elif show_discount and price_list_contains_template:
                base_price = base_sales_prices[template.id]
                base_price = self.env['account.tax']._fix_tax_included_price_company(
                    base_price, product_taxes, taxes, self.env.company)
                base_price = taxes.compute_all(base_price, pricelist.currency_id, 1, template, partner_sudo)[tax_display]

            compare_list_price_low = compare_list_price = self.env['product.pricelist.item'].search([('product_tmpl_id', '=', template.id)],limit=1, order="compare_list_price asc").compare_list_price
            price_reduce = price_reduce2 = self.env['product.pricelist.item'].search([('product_tmpl_id', '=', template.id)],limit=1, order="fixed_price asc").fixed_price
            if template._name == 'product.template':
                product_ids = self.env['product.product'].sudo().search([('product_tmpl_id', '=', template.id)])
                for product_id in product_ids:
                    price_list = self.env['product.pricelist.item'].search([('product_id', '=', product_id.id)], limit=1, order="id desc")
                    price_reduce_check = price_list.fixed_price
                    compare_list_price_check = price_list.compare_list_price
                    if compare_list_price_low > compare_list_price_check:
                        compare_list_price_low = compare_list_price_check
                    if compare_list_price < compare_list_price_check:
                        compare_list_price = compare_list_price_check
                    if price_reduce > price_reduce_check:
                        price_reduce = price_reduce_check
                    if price_reduce2 < price_reduce_check:
                        price_reduce2 = price_reduce_check
            price_reduce = self.env['account.tax']._fix_tax_included_price_company(
                price_reduce, product_taxes, taxes, self.env.company)
            price_reduce = taxes.compute_all(price_reduce, pricelist.currency_id, 1, template, partner_sudo)[tax_display]
            price_reduce2 = self.env['account.tax']._fix_tax_included_price_company(
                price_reduce2, product_taxes, taxes, self.env.company)
            price_reduce2 = taxes.compute_all(price_reduce2, pricelist.currency_id, 1, template, partner_sudo)[tax_display]
            base_price = template.currency_id._convert(
                from_amount=compare_list_price_low,
                to_currency=self.currency_id,
                company=self.env.company,
                date=date,
                round=False)
            base_price2 = template.currency_id._convert(
                from_amount=compare_list_price,
                to_currency=self.currency_id,
                company=self.env.company,
                date=date,
                round=False)
            base_percent = base_percent2 = 0
            if base_price2 == base_price:
                base_price2 = False

            if price_reduce2 == price_reduce:
                price_reduce2 = False
            if base_price2 != 0 and price_reduce2 != 0:
                base_percent2 = 100 - (price_reduce2 * 100 / base_price2)
            if base_price != 0 and price_reduce != 0:
                base_percent = price_reduce * 100 / base_price

            template_price_vals = {'price_reduce': int(price_reduce),'price_reduce2': int(price_reduce2),'base_price': int(base_price),'base_price2': int(base_price2),'base_percent2': int(base_percent2),'base_percent': int(base_percent),}

            res[template.id] = template_price_vals

        return res

    def _get_discount_price_wss(self):
        template = self
        compare_list_price_low = compare_list_price = self.env['product.pricelist.item'].search(
            [('product_tmpl_id', '=', template.id)], limit=1, order="compare_list_price asc").compare_list_price
        price_reduce = price_reduce2 = self.env['product.pricelist.item'].search(
            [('product_tmpl_id', '=', template.id)], limit=1, order="fixed_price asc").fixed_price
        if template._name == 'product.template':
            product_ids = self.env['product.product'].sudo().search([('product_tmpl_id', '=', template.id)])
            for product_id in product_ids:
                price_list = self.env['product.pricelist.item'].search([('product_id', '=', product_id.id)], limit=1,
                                                                       order="id desc")
                price_reduce_check = price_list.fixed_price
                compare_list_price_check = price_list.compare_list_price
                if compare_list_price_low > compare_list_price_check:
                    compare_list_price_low = compare_list_price_check
                if compare_list_price < compare_list_price_check:
                    compare_list_price = compare_list_price_check
                if price_reduce > price_reduce_check:
                    price_reduce = price_reduce_check
                if price_reduce2 < price_reduce_check:
                    price_reduce2 = price_reduce_check
        base_percent = base_percent2 = 0

        if price_reduce2 == price_reduce:
            price_reduce2 = False
        if compare_list_price != 0 and price_reduce2 != 0:
            base_percent2 = 100 - (price_reduce2 * 100 / compare_list_price)
        if compare_list_price_low != 0 and price_reduce != 0:
            base_percent = 100 - (price_reduce * 100 / compare_list_price_low)

        template_price_vals = {'base_percent2': int(round(base_percent2,0)),'base_percent': int(round(base_percent,0)), }
        return template_price_vals



