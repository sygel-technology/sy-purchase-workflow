# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    can_be_secondary = fields.Boolean(default=False)

    secondary_purchase_ids = fields.Many2many(
        string="Secondary Purchases",
        comodel_name="purchase.order",
        relation="purchase_order_secondary_purchases",
        column1="main_purchases",
        column2="secondary_purchases",
    )
    secondary_purchases_count = fields.Integer(
        compute="_compute_secondary_purchases_count", store=True
    )
    main_purchase_ids = fields.Many2many(
        string="Main Purchases",
        comodel_name="purchase.order",
        relation="purchase_order_secondary_purchases",
        column1="secondary_purchases",
        column2="main_purchases",
    )
    main_purchases_count = fields.Integer(
        compute="_compute_main_purchases_count", store=True
    )

    @api.depends("main_purchase_ids")
    def _compute_main_purchases_count(self):
        for rec in self:
            rec.main_purchases_count = len(rec.main_purchase_ids)

    @api.depends("secondary_purchase_ids")
    def _compute_secondary_purchases_count(self):
        for rec in self:
            rec.secondary_purchases_count = len(rec.secondary_purchase_ids)

    def action_create_related_wizard(self):
        not_allowed_purchases = self.filtered(lambda p: p.main_purchase_ids)
        if not_allowed_purchases:
            raise exceptions.ValidationError(
                _(
                    "The following purchases can not be linked to secondary purchases, "
                    "due to already being a secondary purchase: {}"
                ).format(", ".join(not_allowed_purchases.mapped("name")))
            )
        return {
            "name": _("Create/Link Secondary Purchases"),
            "type": "ir.actions.act_window",
            "res_model": "purchase.order.secondary.linker",
            "view_mode": "form",
            "target": "new",
            "context": {"main_purchase_ids": self.ids},
        }

    def action_secondary_purchase(self):
        return {
            "name": _("Secondary Purchase"),
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "view_mode": "tree,form",
            "domain": [("id", "in", self.secondary_purchase_ids.ids)],
        }

    def action_main_purchases(self):
        return {
            "name": _("Main Purchases"),
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "view_mode": "tree,form",
            "domain": [("id", "in", self.main_purchase_ids.ids)],
        }
