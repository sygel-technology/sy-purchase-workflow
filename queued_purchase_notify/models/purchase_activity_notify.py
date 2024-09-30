# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PurchaseActivityNotify(models.Model):
    _name = "purchase.activity.notify"
    _description = "Purchase Mail Notify"

    time_after_confirmation = fields.Float(name="Time After Confirmation (Hours)")
    time_to_deadline = fields.Integer(name="Days to Deadline")
    summary = fields.Char(name="Summary")
    note = fields.Char(name="Note")
    purchase_order_type_id = fields.Many2one(
        name="Purchase Order Type", comodel_name="purchase.order.type"
    )
    user_id = fields.Many2one(string="User", comodel_name="res.users")
