# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PurchaseSplitWizard(models.TransientModel):
    _inherit = "purchase.split.wizard"

    picking_type_id = fields.Many2one(
        comodel_name="stock.picking.type",
        string="Deliver to",
        domain="['|', ('warehouse_id', '=', False),"
        "('warehouse_id.company_id', '=', company_id)]",
    )

    def _get_new_purchase_vals(self):
        vals = super()._get_new_purchase_vals()
        if self.picking_type_id:
            vals["picking_type_id"] = self.picking_type_id.id
        return vals
