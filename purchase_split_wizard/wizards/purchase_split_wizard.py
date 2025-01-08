# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models


class PurchaseSplitWizard(models.TransientModel):
    _name = "purchase.split.wizard"
    _description = "Wizard to split purchases"

    purchase_origin_id = fields.Many2one(
        string="Purchase", comodel_name="purchase.order", readonly=True
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        related="purchase_origin_id.company_id",
    )
    partner_id = fields.Many2one(
        string="Vendor",
        comodel_name="res.partner",
        ondelete="restrict",
        required=True,
    )
    product_price_option = fields.Selection(
        selection=[("purchase", "Purchase Order Price"), ("product", "Product Price")],
        required=True,
        default="product",
    )

    partner_ref = fields.Char(string="Vendor Reference")

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        required=True,
    )
    date_order = fields.Datetime(
        string="Order Deadline",
        required=True,
    )
    date_planned = fields.Datetime(
        string="Expected Arrival",
    )
    origin = fields.Char(string="Source Document")
    incoterm_id = fields.Many2one(comodel_name="account.incoterms", string="Incoterm")
    payment_term_id = fields.Many2one(
        comodel_name="account.payment.term",
        string="Payment Terms",
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )
    payment_mode_id = fields.Many2one(
        comodel_name="account.payment.mode",
        string="Payment Mode",
        domain="[('payment_type', '=', 'outbound'), ('company_id', '=', company_id)]",
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Buyer",
    )
    wizard_line_ids = fields.One2many(
        string="Purchase lines",
        comodel_name="purchase.line.split.wizard",
        inverse_name="wizard_id",
    )

    @api.model
    def get_default_lines(self, purchase_id):
        return [
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
            for line in purchase_id.order_line
            if line.qty_splittable or line.display_type
        ]

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        purchase_id = self.env["purchase.order"].browse(
            res.get("purchase_origin_id")
            or self.env.context.get("default_purchase_origin_id")
        )
        wizard_line_ids = self.get_default_lines(purchase_id)
        res.update(
            {
                "partner_id": purchase_id.partner_id.id,
                "partner_ref": False,
                "currency_id": purchase_id.currency_id,
                "date_order": purchase_id.date_order,
                "date_planned": purchase_id.date_planned,
                "origin": purchase_id.name,
                "incoterm_id": False,
                "payment_term_id": (
                    purchase_id.partner_id.property_supplier_payment_term_id
                ),
                "payment_mode_id": purchase_id.partner_id.supplier_payment_mode_id,
                "user_id": purchase_id.user_id,
                "wizard_line_ids": wizard_line_ids,
            }
        )
        return res

    def _get_new_purchase_vals(self):
        return {
            "splitted_purchase_parent_id": self.purchase_origin_id.id,
            "partner_id": self.partner_id.id,
            "partner_ref": self.partner_ref,
            "currency_id": self.currency_id.id,
            "date_order": self.date_order,
            "date_planned": self.date_planned,
            "origin": self.origin,
            "incoterm_id": self.incoterm_id.id,
            "payment_term_id": self.payment_term_id.id,
            "payment_mode_id": self.payment_mode_id.id,
            "user_id": self.user_id.id,
            "order_line": [
                (
                    0,
                    0,
                    {
                        "product_id": line.product_id.id,
                        "name": line.name,
                        "product_qty": line.product_qty,
                        "qty_splitted": line.product_qty,
                        "splitted_purchase_line_parent_id": (
                            line.purchase_line_origin_id.id
                        ),
                        "price_unit": (
                            line.purchase_line_origin_id.price_unit
                            if line.wizard_id.product_price_option == "purchase"
                            else False
                        ),
                        "display_type": line.display_type,
                    },
                )
                for line in self.wizard_line_ids
                if line.product_qty > 0 or line.display_type
            ],
        }

    def action_accept(self):
        vals = self._get_new_purchase_vals()
        new_purchase = self.env["purchase.order"].create(vals)
        self.purchase_origin_id.write({"active": False, "state": "cancel"})
        return {
            "name": _("Splitted Purchase"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "purchase.order",
            "target": "current",
            "res_id": new_purchase.id,
        }


class PurchaseLineSplitWizard(models.TransientModel):
    _name = "purchase.line.split.wizard"
    _description = "Wizard aux model to split purchase lines"

    wizard_id = fields.Many2one(
        string="Wizard",
        comodel_name="purchase.split.wizard",
    )
    purchase_line_origin_id = fields.Many2one(
        string="Purchase Line", comodel_name="purchase.order.line", readonly=True
    )
    sequence = fields.Integer(required=True)
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    name = fields.Text()
    product_qty = fields.Float(
        string="Quantity", digits="Product Unit of Measure", required=True, default=0.0
    )
    max_product_qty = fields.Float(
        string="Max Quantity",
        related="purchase_line_origin_id.qty_splittable",
        digits="Product Unit of Measure",
        readonly=True,
    )
    display_type = fields.Selection(
        selection=[("line_section", "Section"), ("line_note", "Note")],
        default=False,
    )

    @api.constrains("product_qty")
    def _check_max_qty(self):
        for rec in self:
            if rec.product_qty > rec.max_product_qty:
                raise exceptions.ValidationError(
                    _("The quantity can not be higher than the max quantity")
                )
