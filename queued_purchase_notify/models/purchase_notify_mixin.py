# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PurchaseNotifyMixin(models.AbstractModel):
    _name = "purchase.notify.mixin"
    _description = "Mixin for queued purchase notification events"

    _inherit = "notify.mixin"

    notified_model_name = "purchase.order"

    trigger_state = fields.Selection(
        selection_add=[
            ("purchase", "Confirmed Purchases"),
        ],
        default="purchase",
        required=True,
        ondelete={
            "purchase": "cascade",
        },
    )

    purchase_order_type_id = fields.Many2one(
        name="Purchase Order Type", comodel_name="purchase.order.type"
    )

    def is_to_notify(self, record):
        # Returns if a record is in a status to be notified
        if self.trigger_state == "purchase":
            return record.state in ["purchase", "done"]
        else:
            return False
