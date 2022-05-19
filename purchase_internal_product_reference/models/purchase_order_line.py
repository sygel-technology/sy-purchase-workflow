# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _get_product_purchase_description(self, product_lang):
        self.ensure_one()
        return super(
                PurchaseOrderLine, self
            )._get_product_purchase_description(
            product_lang.with_context(avoid_internal_name=True)
        )
