# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PurchaseLogNoteNotify(models.Model):
    _name = "purchase.log.note.notify"
    _description = "Purchase Mail Notify"

    time_after_confirmation = fields.Float(name="Time After Confirmation (Hours)")
    note_text = fields.Char(name="Note Text")
    purchase_order_type_id = fields.Many2one(
        name="Purchase Order Type", comodel_name="purchase.order.type"
    )
