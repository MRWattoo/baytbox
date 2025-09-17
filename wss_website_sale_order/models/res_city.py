# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class ResCity(models.Model):
    _name = 'res.city'
    _description = 'City'

    name = fields.Char(string="Name")
    code = fields.Char(string="City Code")
    state_id = fields.Many2one('res.country.state',string="State")
    country_id = fields.Many2one('res.country',related="state_id.country_id",string="Country")
    active = fields.Boolean(string="Active", related="country_id.active")
    website_visible = fields.Boolean(string="Website Visible", related="country_id.website_visible")


class ResDistrict(models.Model):
    _name = 'res.district'
    _description = 'District'

    name = fields.Char(string="Name")
    code = fields.Char(string="District Code")
    city_id = fields.Many2one('res.city',string="City")
    state_id = fields.Many2one('res.country.state',related="city_id.state_id",string="State")

    country_id = fields.Many2one('res.country',related="city_id.country_id",string="Country")
    active = fields.Boolean(string="Active", related="country_id.active")
    website_visible = fields.Boolean(string="Website Visible", related="country_id.website_visible")


class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    active = fields.Boolean(string="Active", related="country_id.active")
    website_visible = fields.Boolean(string="Website Visible", related="country_id.website_visible")
    dist_ids = fields.One2many('res.district','state_id',string="Districts")
    city_ids = fields.One2many('res.city','state_id',string="Cities")

class ResCountryState(models.Model):
    _inherit = 'res.partner'

    dist_id = fields.Many2one('res.district', string="District", domain="[('city_id','=',city_id)]")
    city_id = fields.Many2one('res.city', string="City", domain="[('state_id','=',state_id)]")
