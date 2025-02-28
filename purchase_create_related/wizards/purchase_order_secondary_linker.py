# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models


class PurchaseOrderSecondaryLinker(models.TransientModel):
    _name = "purchase.order.secondary.linker"
    _description = "Wizard to link purchases to secondary purchases"

    operation_type = fields.Selection(
        selection=[
            ("create", "Create Quotation Purchase"),
            ("link", "Link to Quotation Purchase"),
        ],
        required=True,
    )

    main_purchase_ids = fields.Many2many(
        string="Main Purchases",
        comodel_name="purchase.order",
        domain=[
            ("main_purchase_ids", "=", False),
        ],
        required=True,
    )
    secondary_purchase_id = fields.Many2one(
        string="Secondary Purchase",
        comodel_name="purchase.order",
        domain=[
            ("secondary_purchase_ids", "=", False),
            ("can_be_secondary", "!=", False),
            ("state", "in", ["draft", "sent", "to approve"]),
        ],
    )
    partner_id = fields.Many2one(
        string="Secondary Purchase Partner",
        comodel_name="res.partner",
    )

    def default_get(self, fields):
        vals = super().default_get(fields)
        main_purchase_ids = (
            self.env["purchase.order"]
            .browse(self.env.context.get("main_purchase_ids"))
            .exists()
        )
        if main_purchase_ids:
            vals["main_purchase_ids"] = [(4, p_id) for p_id in main_purchase_ids.ids]
            vals["partner_id"] = main_purchase_ids.partner_id[:1].id
        return vals

    @api.constrains("secondary_purchase_id")
    def _check_secondary_purchase_id(self):
        if self.secondary_purchase_id.filtered(
            lambda s: s.id in self.main_purchase_ids.ids
        ):
            raise exceptions.ValidationError(
                _("A purchase can't be main and secondary at the same time")
            )

    def action_accept(self):
        self.ensure_one()
        if self.operation_type == "create":
            return self._create_secondary_purchases()
        elif self.operation_type == "link":
            self._link_secondary_purchases()

    def _link_secondary_purchases(self, secondary_purchase_id=False):
        self.ensure_one()
        if not secondary_purchase_id:
            secondary_purchase_id = self.secondary_purchase_id
        self.main_purchase_ids.write(
            {"secondary_purchase_ids": [(4, secondary_purchase_id.id)]}
        )

    def get_new_purchase_vals(self):
        return {
            "partner_id": self.partner_id.id,
            "can_be_secondary": True,
        }

    def _create_secondary_purchases(self):
        new_purchase = self.env["purchase.order"].create(self.get_new_purchase_vals())
        self._link_secondary_purchases(new_purchase)
        return {
            "name": _("Secondary Purchase"),
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "view_mode": "form",
            "res_id": new_purchase.id,
        }
