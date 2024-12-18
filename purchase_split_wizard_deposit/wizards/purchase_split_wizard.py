# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models


class PurchaseSplitWizard(models.TransientModel):
    _inherit = "purchase.split.wizard"

    split_advances = fields.Boolean()

    advance_line_ids = fields.One2many(
        string="Advance lines",
        comodel_name="purchase.advance.line.split.wizard",
        inverse_name="wizard_id",
    )

    def get_default_lines(self, purchase_id):
        old_res = super().get_default_lines(purchase_id)
        advance_line_ids = purchase_id.order_line.filtered("is_deposit").mapped("id")
        new_res = []
        for command in old_res:
            if command[2].get("purchase_line_origin_id") not in advance_line_ids:
                new_res.append(command)
        return new_res

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        purchase_id = self.env["purchase.order"].browse(
            res.get("purchase_origin_id")
            or self.env.context.get("default_purchase_origin_id")
        )
        splitteable_advance_lines = purchase_id.order_line.filtered(
            lambda li: ((li.qty_splittable or li.display_type) and li.is_deposit)
        )
        res.update(
            {
                "split_advances": any(splitteable_advance_lines),
                "advance_line_ids": [
                    (
                        0,
                        0,
                        {
                            "wizard_id": self.id,
                            "product_id": line.product_id,
                            "name": line.name,
                            "purchase_line_origin_id": line.id,
                            "display_type": line.display_type,
                        },
                    )
                    for line in splitteable_advance_lines
                ],
            }
        )
        return res

    def _get_new_purchase_vals(self):
        res = super()._get_new_purchase_vals()
        if self.split_advances:
            res["order_line"] += [
                (
                    0,
                    0,
                    {
                        "product_id": line.product_id.id,
                        "name": line.name,
                        "product_qty": 0,
                        "qty_splitted": line.amount,
                        "price_unit": line.amount,
                        "splitted_purchase_line_parent_id": (
                            line.purchase_line_origin_id.id
                        ),
                        "date_planned": line.purchase_line_origin_id.date_planned,
                        "display_type": line.display_type,
                        "is_deposit": True,
                    },
                )
                for line in self.advance_line_ids
                if line.amount or line.display_type
            ]
        return res


class PurchaseAdvanceLineSplitWizard(models.TransientModel):
    _name = "purchase.advance.line.split.wizard"
    _description = "Wizard aux model to split purchase lines"

    wizard_id = fields.Many2one(
        string="Wizard",
        comodel_name="purchase.split.wizard",
    )
    purchase_line_origin_id = fields.Many2one(
        string="Purchase Line", comodel_name="purchase.order.line", readonly=True
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    name = fields.Text()
    currency_id = fields.Many2one(
        related="purchase_line_origin_id.order_id.currency_id",
        string="Currency",
        readonly=True,
    )
    amount = fields.Monetary()
    max_amount = fields.Monetary(compute="_compute_max_amount", readonly=True)
    display_type = fields.Selection(
        selection=[("line_section", "Section"), ("line_note", "Note")],
        default=False,
    )

    @api.depends("purchase_line_origin_id")
    def _compute_max_amount(self):
        for rec in self:
            rec.max_amount = rec.purchase_line_origin_id.qty_splittable

    @api.constrains("amount", "max_amount")
    def _check_max_amount(self):
        for rec in self:
            if not rec.display_type and rec.amount > rec.max_amount:
                raise exceptions.ValidationError(
                    _("The amount can not be higher than the max amount.")
                )
