# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    mail_queue_ids = fields.Many2many(
        string="Purchase Queues",
        comodel_name="queue.job",
        compute="_compute_mail_queues",
    )

    def button_confirm(self):
        res = super().button_confirm()
        notity_set = self.order_type._get_purchase_notify_ids()
        for notify_ids in notity_set.values():
            for notify_id in notify_ids:
                for rec in self:
                    if notify_id.is_to_notify(rec):
                        notify_id.notify(rec)
        return res

    def _compute_mail_queues(self):
        for obj in self:
            obj.mail_queue_ids = (
                self.env["queue.job"]
                .search(
                    [
                        [
                            "func_string",
                            "=like",
                            f"purchase.mail.notify(%,)._notify_thread(purchase.order({obj.id},))",
                        ]
                    ]
                )
                .ids
            )
