from odoo import models, fields


class partner(models.Model):
    _inherit = "res.partner"

    x_studio_phone_2 = fields.Char(string="Phone 2")
    # phone_whatsapp = fields.Char(string="Mobile Whatsappp",compute="compute_phone_whatsapp")
    #
    #
    # @api.depends('mobile')
    # def compute_mobile_whatsapp(self):
    #     for rec in self:
    #         if rec.mobile:
    #             if rec.mobile[0] == '+':
    #                 rec.mobile_whatsapp = f"https://web.whatsapp.com/send?phone={rec.mobile}&text="
    #             else:
    #                 rec.mobile_whatsapp = f"https://web.whatsapp.com/send?phone=+{rec.mobile}&text="
    #         else:
    #             rec.mobile_whatsapp = ''
    #
    # @api.depends('phone')
    # def compute_phone_whatsapp(self):
    #     for rec in self:
    #         if rec.phone:
    #             if rec.phone[0] == '+':
    #                 rec.phone_whatsapp = f"https://web.whatsapp.com/send?phone={rec.phone}&text="
    #             else:
    #                 rec.phone_whatsapp = f"https://web.whatsapp.com/send?phone=+{rec.phone}&text="
    #         else:
    #             rec.phone_whatsapp = ''

    def send_message_mobile(self):
        if self.mobile:
            number = self.mobile
            link = "https://web.whatsapp.com/send?phone=" + number
            send_msg = {
                'type': 'ir.actions.act_url',
                'url': link + "&text=",
                'target': 'new',
                'res_id': self.id,
            }

            return send_msg
    def send_message_phone(self):
        if self.phone:
            number = self.phone
            link = "https://web.whatsapp.com/send?phone=" + number
            send_msg = {
                'type': 'ir.actions.act_url',
                'url': link + "&text=",
                'target': 'new',
                'res_id': self.id,
            }

            return send_msg
    def send_message_phone2(self):
        if self.x_studio_phone_2:
            number = self.x_studio_phone_2
            link = "https://web.whatsapp.com/send?phone=" + number
            send_msg = {
                'type': 'ir.actions.act_url',
                'url': link + "&text=",
                'target': 'new',
                'res_id': self.id,
            }

            return send_msg
