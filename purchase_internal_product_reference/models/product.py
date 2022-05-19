# Copyright 2022 Angel Garcia de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def name_get(self):
        if not self.env.context.get("avoid_internal_name") and (
            self.env.company.internal_ref_product or 
            "default_description_sale" in self.env.context
        ):
            ctx = self.env.context.copy()
            ctx.update({'partner_id': False})
            result = super(ProductProduct, self.with_context(ctx)).name_get()
        else:
            result = super().name_get()
        return result
