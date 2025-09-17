# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api, _
import logging

class ResCountry(models.Model):
    _inherit = 'res.country'

    active = fields.Boolean(string="Active")
    website_visible = fields.Boolean(string="Website Visible")
    website_ids = fields.Many2many('website', string="Websites")

