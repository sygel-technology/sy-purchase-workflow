# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PurchaseSplitWizard(models.TransientModel):
    _inherit = "purchase.split.wizard"

    order_type = fields.Many2one(
        string="Purchase Order Type",
        comodel_name="purchase.order.type",
        required=True,
    )

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        purchase_id = self.env["purchase.order"].browse(
            res.get("purchase_origin_id")
            or self.env.context.get("default_purchase_origin_id")
        )
        res.update(
            {
                "order_type": purchase_id.order_type,
            }
        )
        return res

    def _get_new_purchase_vals(self):
        vals = super()._get_new_purchase_vals()
        vals["order_type"] = self.order_type.id
        return vals
