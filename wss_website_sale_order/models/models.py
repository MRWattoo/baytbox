from odoo import http,models
from odoo.http import request, route
import logging
import json
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.website.controllers.main import Website
import re
_logger = logging.getLogger(__name__)

from markupsafe import Markup

class WebsiteInherit(Website):


    @http.route([
        '/website/search',
        '/website/search/page/<int:page>',
        '/website/search/<string:search_type>',
        '/website/search/<string:search_type>/page/<int:page>',
    ], type='http', auth="public", website=True, sitemap=False)
    def hybrid_list(self, page=1, search='', search_type='all', **kw):
        if not search:
            return request.render("website.list_hybrid")
        options = self._get_hybrid_search_options(**kw)
        data = self.autocomplete(search_type=search_type, term=search, order='name asc', limit=500, max_nb_chars=200, options=options)

        results = data.get('results', [])
        search_count = len(results)
        parts = data.get('parts', {})

        step = 50
        pager = portal_pager(
            url="/website/search/%s" % search_type,
            url_args={'search': search},
            total=search_count,
            page=page,
            step=step
        )

        results = results[(page - 1) * step:page * step]
        for result in results:
            # logger.info(result.get('detail'))
            if result.get('image_url') and 'product.template' in result.get('image_url'):
                website_url = result.get('website_url')
                if website_url:
                    raw_list_int = list(map(int, re.findall(r'\d+', website_url)))
                    product_tmpl_id = raw_list_int[-1]  # Get the last number which is the product template ID
                    template = request.env['product.template'].search([('id', '=', product_tmpl_id)])
                    website = request.env['website'].get_current_website()
                    pricelist = website.pricelist_id
                    fiscal_position = website.fiscal_position_id.sudo()
                    prices = template._get_sales_prices(pricelist, fiscal_position)

                    if prices:
                        currency_symbol = pricelist.currency_id.symbol
                        currency_position = pricelist.currency_id.position

                        base_price = prices[product_tmpl_id].get('base_price', 0.0)
                        base_price2 = prices[product_tmpl_id].get('base_price2', 0.0)
                        price_reduce = prices[product_tmpl_id].get('price_reduce', 0.0)
                        price_reduce2 = prices[product_tmpl_id].get('price_reduce2', 0.0)
                        base_percent2 = prices[product_tmpl_id].get('base_percent2', 0.0)

                        base_percent2_text = ''
                        if base_percent2 > 0:
                            base_percent2_text = f'<div class="o_tag">{base_percent2}% off</div>'

                        base_price_text = ''
                        if base_price and base_price2 and price_reduce and price_reduce2:
                            base_price_text = f'<div><del class="text-muted me-1 h6 mb-0" style="white-space: nowrap;"><em class="small">{base_price}</em><span>{currency_symbol}</span><em class="small">{base_price2}</em><span>{currency_symbol}</span></del></div>'
                        elif base_price > price_reduce:
                            base_price_text = f'<div><del class="text-muted me-1 h6 mb-0" style="white-space: nowrap;"><em class="small">{base_price}</em><span>{currency_symbol}</span></del></div>'
                        elif base_price2 > price_reduce2:
                            base_price_text = f'<div><del class="text-muted me-1 h6 mb-0" style="white-space: nowrap;"><em class="small">{base_price2}</em><span>{currency_symbol}</span></del></div>'

                        reduce_price_text = ''
                        if base_price and base_price2 and price_reduce and price_reduce2:
                            reduce_price_text = f'<div><span class="h6 mb-0">{price_reduce}</span><span>{currency_symbol}</span><span class="h6 mb-0">-</span><span class="h6 mb-0">{price_reduce2}</span><span>{currency_symbol}</span></div>'
                        elif base_price2 > price_reduce2:
                            reduce_price_text = f'<div><span class="h6 mb-0">{price_reduce2}</span><span>{currency_symbol}</span></div>'
                        elif price_reduce2:
                            reduce_price_text = f'<div><span class="h6 mb-0">{price_reduce2}</span><span>{currency_symbol}</span></div>'

                        # Construct the HTML content
                        html_content = f"{base_percent2_text}{base_price_text}{reduce_price_text}"
                        result['detail'] = Markup(html_content)

                        _logger.info('Updated result detail:')
                        _logger.info(result['detail'])
        values = {
            'pager': pager,
            'results': results,
            'parts': parts,
            'search': search,
            'fuzzy_search': data.get('fuzzy_search'),
            'search_count': search_count,
        }
        return request.render("website.list_hybrid", values)

class CustomerPortalWSS(CustomerPortal):
    MANDATORY_BILLING_FIELDS = ["name", "phone", "email", "street", "city","city_id","dist_id", "country_id"]

    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })
        if post and request.httprequest.method == 'POST':
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                values = {key: post[key] for key in self._get_mandatory_fields()}
                values.update({key: post[key] for key in self._get_optional_fields() if key in post})
                for field in set(['country_id', 'state_id','city_id','dist_id']) & set(values.keys()):
                    try:
                        values[field] = int(values[field])
                    except:
                        values[field] = False
                values.update({'zip': values.pop('zipcode', '')})
                self.on_account_update(values, partner)
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])
        city = partner.city_id
        cities = request.env['res.city'].search([('state_id','=',partner.state_id.id)])
        dist = partner.dist_id
        dists = request.env['res.district'].search([('city_id','=',city.id)])
        values.update({
            'partner': partner,
            'countries': countries,
            'states': states,
            'district_city': cities,
            'state_district': dists,
            'city_id': city.id,
            'dist_id': dist.id,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'partner_can_edit_vat': partner.can_edit_vat(),
            'redirect': redirect,
            'page_name': 'my_details',
        })
        response = request.render("portal.portal_my_details", values)
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
        return response

class FormController(http.Controller):

    @http.route('/get_districts', type='json', auth='public', methods=['POST'])
    def get_districts(self, **kwargs):
        raw_data = request.httprequest.data
        data = json.loads(raw_data)
        city_id = data.get('city_id')
        if city_id:
            dist_ids = request.env['res.district'].sudo().search([('city_id', '=', int(city_id))])
            districts = [{'id': district.id, 'name': district.name} for district in dist_ids]
            return {'districts': districts}
        return {'districts': []}

    @http.route('/get_cities', type='json', auth='public', methods=['POST'])
    def get_cities(self, **kwargs):
        raw_data = request.httprequest.data
        data = json.loads(raw_data)
        district_id = data.get('state_id')
        if district_id:
            city_ids = request.env['res.city'].sudo().search([('state_id', '=', int(district_id))])
            cities = [{'id': city.id, 'name': city.name} for city in city_ids]
            return {'cities': cities}
        return {'cities': []}
