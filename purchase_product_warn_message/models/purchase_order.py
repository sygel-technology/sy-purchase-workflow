# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ModelName(models.Model):
    _inherit = "purchase.order"

    purchase_product_warn_msg = fields.Html(
        compute="_compute_purchase_product_warn_msg"
    )

    @api.depends("state", "order_line.product_id")
    def _compute_purchase_product_warn_msg(self):
        for rec in self:
            purchase_product_warn_msg = ""
            separator = "<br/>"
            if rec.order_line:
                if rec.state in ["done", "cancel"]:
                    rec.purchase_product_warn_msg = ""
                    continue
                warnable_products = rec.order_line.mapped("product_id").filtered(
                    lambda p: p.purchase_line_warn == "warning"
                )
                purchase_product_warn_msg = separator.join(
                    [
                        f"<b>{product_id.display_name}: </b>"
                        f"<span>{product_id.purchase_line_warn_msg}</span>"
                        for product_id in warnable_products
                    ]
                )
            rec.purchase_product_warn_msg = purchase_product_warn_msg
