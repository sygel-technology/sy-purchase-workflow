# Copyright 2026 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class Http(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        res = super().session_info()
        res.update(
            {
                "purchase_order_line_display_number": self.env.ref(
                    "purchase_order_line_display_number.purchase_order_line_display_number"
                )
                .sudo()
                .value
            }
        )
        return res
