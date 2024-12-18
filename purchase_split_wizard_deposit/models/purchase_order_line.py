# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.depends("qty_invoiced")
    def _compute_qty_splittable(self):
        downpayments = self.filtered(
            lambda li: li.product_id
            == li.order_id.company_id.purchase_deposit_product_id
        )
        for rec in downpayments:
            rec.qty_splittable = (
                rec.qty_invoiced * rec.price_unit - rec.qty_splitted_total
            )
        return super(PurchaseOrderLine, self - downpayments)._compute_qty_splittable()

    @api.depends("splitted_purchase_line_parent_id")
    def _compute_qty_invoiced(self):
        splitted_downpayments = self.filtered(
            lambda li: (
                li.product_id == li.order_id.company_id.purchase_deposit_product_id
                and li.splitted_purchase_line_parent_id
            )
        )
        for rec in splitted_downpayments:
            rec.qty_invoiced = rec.splitted_purchase_line_parent_id.qty_invoiced
            rec.qty_to_invoice = rec.product_qty - rec.qty_invoiced
        return super(
            PurchaseOrderLine, self - splitted_downpayments
        )._compute_qty_invoiced()
