from odoo import models, fields, api
import logging
from PIL import Image, ImageOps
from PIL import IcoImagePlugin
from random import randrange
from odoo.exceptions import UserError
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

try:
    from PIL.Image import Transpose, Palette, Resampling
except ImportError:
    Transpose = Palette = Resampling = Image

Image.preinit()
Image._initialized = 2

FILETYPE_BASE64_MAGICWORD = {
    b'/': 'jpg',
    b'R': 'gif',
    b'i': 'png',
    b'P': 'svg+xml',
}

EXIF_TAG_ORIENTATION = 0x112
EXIF_TAG_ORIENTATION_TO_TRANSPOSE_METHODS = {
    0: [],
    1: [],
    2: [Transpose.FLIP_LEFT_RIGHT],
    3: [Transpose.ROTATE_180],
    4: [Transpose.FLIP_TOP_BOTTOM],
    5: [Transpose.FLIP_LEFT_RIGHT, Transpose.ROTATE_90],
    6: [Transpose.ROTATE_270],
    7: [Transpose.FLIP_TOP_BOTTOM, Transpose.ROTATE_90],
    8: [Transpose.ROTATE_90],
}

IMAGE_MAX_RESOLUTION = 50e6


class AccountMove(models.Model):
    _inherit = 'account.move'

    total_qty_billed = fields.Float(string="Invoiced Qty",compute="compute_total_qty_billed")

    @api.depends('invoice_line_ids')
    def compute_total_qty_billed(self):
        for rec in self:
            rec.total_qty_billed = sum(rec.invoice_line_ids.filtered(lambda t:t.is_landed_costs_line == False).mapped('quantity')) or 0.0

    def image_data_uri(self, base64_source):
        import base64

        aa = str(type(base64_source))
        if 'str' in aa:
            base64_source = bytes(base64_source, 'utf-8')

        return 'data:image/%s;base64,%s' % (
            FILETYPE_BASE64_MAGICWORD.get(base64_source[:1], 'png'),
            base64_source.decode(),
        )
