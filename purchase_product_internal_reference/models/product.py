# Copyright 2022 Angel Garcia de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.depends("company_id.internal_ref_product")
    @api.depends_context("partner_id")
    def _compute_display_name(self):
        if self.env.company.internal_ref_product:
            self_ctx = self.with_context(partner_id=False)
            super(ProductProduct, self_ctx)._compute_display_name()

            for record in self:
                record.display_name = self_ctx.browse(record.id).display_name
        else:
            super()._compute_display_name()
        return None
