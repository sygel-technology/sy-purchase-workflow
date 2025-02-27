# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    zero_purchase_price = fields.Boolean(default=False)

    @api.model
    def _commercial_fields(self):
        return super()._commercial_fields() + [
            "zero_purchase_price",
        ]
