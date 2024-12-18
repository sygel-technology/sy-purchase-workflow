# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import _, api, exceptions, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    splitted_purchase_parent_id = fields.Many2one(
        string="Splitted Purchase Origin",
        comodel_name="purchase.order",
        ondelete="restrict",
    )
    splitted_purchase_children_ids = fields.One2many(
        string="Splitted Purchase Childrens",
        comodel_name="purchase.order",
        inverse_name="splitted_purchase_parent_id",
    )
    splitted_purchase_children_count = fields.Integer(
        string="Splitted Purchases Count",
        compute="_compute_splitted_purchase_children_count",
    )
    split_status = fields.Selection(
        selection=[
            ("none", "None"),
            ("children", "Children"),
            ("parent_partially", "In Progress"),
            ("parent_splitted", "Splitted"),
        ],
        compute="_compute_split_status",
        store=True,
        default="none",
    )

    @api.depends("splitted_purchase_children_ids")
    def _compute_splitted_purchase_children_count(self):
        for rec in self:
            rec.splitted_purchase_children_count = len(
                rec.splitted_purchase_children_ids
            )

    @api.depends("splitted_purchase_children_ids", "splitted_purchase_parent_id")
    def _compute_split_status(self):
        for rec in self:
            status = "none"
            if rec.splitted_purchase_parent_id:
                status = "children"
            if rec.splitted_purchase_children_ids:
                if rec.splitted_purchase_children_ids and any(
                    rec.order_line.filtered(lambda li: li.qty_splittable)
                ):
                    status = "parent_partially"
                else:
                    status = "parent_splitted"
            rec.split_status = status

    def button_split(self):
        self.ensure_one()
        return {
            "name": _("Purchase Split Wizard"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "purchase.split.wizard",
            "target": "new",
            "context": {"default_purchase_origin_id": self.id},
        }

    def action_view_splitted_purchase_parent_id(self):
        self.ensure_one()
        return {
            "name": _("Splitted Purchase Origin"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "purchase.order",
            "target": "current",
            "res_id": self.splitted_purchase_parent_id.id,
        }

    def action_view_splitted_purchase_children_ids(self):
        self.ensure_one()
        return {
            "name": _("Splitted Purchases"),
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "res_model": "purchase.order",
            "target": "current",
            "domain": [("id", "in", self.splitted_purchase_children_ids.ids)],
        }

    def toggle_active(self):
        if self.filtered(
            lambda p: p.split_status in ["parent_partially", "parent_splitted"]
        ):
            raise exceptions.ValidationError(
                _("You can not change active status of splitted purchases")
            )
        return super().toggle_active()

    def button_confirm(self):
        if self.filtered(
            lambda p: p.split_status in ["parent_partially", "parent_splitted"]
        ):
            raise exceptions.ValidationError(
                _("You can not confirm splitted purchases")
            )
        return super().button_confirm()

    def unlink(self):
        parent_ids = self.mapped("splitted_purchase_parent_id")
        res = super().unlink()
        for rec in parent_ids.filtered(lambda p: not p.splitted_purchase_children_ids):
            rec.write(
                {
                    "state": "draft",
                    "active": True,
                }
            )
        return res
