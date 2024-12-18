# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _make_po_get_domain(self, company_id, values, partner):
        # Don't automatically edit splitted purchases
        return super()._make_po_get_domain(company_id, values, partner) + (
            ("split_status", "=", "none"),
        )
