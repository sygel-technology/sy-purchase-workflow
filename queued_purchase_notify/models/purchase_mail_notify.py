# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class PurchaseMailNotify(models.Model):
    _name = "purchase.mail.notify"
    _description = "Purchase Mail Notify"

    time_after_confirmation = fields.Float(
        name="Time After Confirmation (Hours)"
    )
    mail_template_id = fields.Many2one(
        name="Mail Template",
        comodel_name="mail.template",
        domain="[('model_id.model', '=', 'purchase.order')]"
    )
    purchase_order_type_id = fields.Many2one(
        name="Purchase Order Type",
        comodel_name="purchase.order.type"
    )
