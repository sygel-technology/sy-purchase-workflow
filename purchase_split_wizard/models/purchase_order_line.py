# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    qty_splitted_total = fields.Float(
        string="Qty Splitted (Total)",
        compute="_compute_qty_splitted_total",
        store=True,
    )
    qty_splitted = fields.Float(
        readonly=True,
    )
    qty_splittable = fields.Float(compute="_compute_qty_splittable")
    splitted_purchase_line_parent_id = fields.Many2one(
        string="Splitted Purchase Line Origin",
        comodel_name="purchase.order.line",
    )
    split_status = fields.Selection(related="order_id.split_status")

    @api.depends("product_qty", "order_id.splitted_purchase_children_ids")
    def _compute_qty_splitted_total(self):
        for rec in self:
            qty_splitted_total = 0
            for line in rec.order_id.splitted_purchase_children_ids.order_line.filtered(
                lambda li, rec=rec: li.splitted_purchase_line_parent_id == rec
            ):
                qty_splitted_total += line.qty_splitted
            rec.qty_splitted_total = qty_splitted_total

    @api.depends("product_qty", "qty_splitted_total")
    def _compute_qty_splittable(self):
        for rec in self:
            rec.qty_splittable = rec.product_qty - rec.qty_splitted_total
