# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _prepare_purchase_order(
        self, product_id, product_qty, product_uom, origin, values, partner
    ):
        values = super()._prepare_purchase_order(
            product_id, product_qty, product_uom, origin, values, partner
        )
        if partner.purchase_type:
            values["order_type"] = partner.purchase_type.id
        return values
