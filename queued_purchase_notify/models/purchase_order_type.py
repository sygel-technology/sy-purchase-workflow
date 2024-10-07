# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PurchaseOrderType(models.Model):
    _inherit = "purchase.order.type"

    purchase_mail_notify_ids = fields.One2many(
        name="Purchase Mail Notifications",
        comodel_name="purchase.mail.notify",
        inverse_name="purchase_order_type_id",
    )
    purchase_log_note_notify_ids = fields.One2many(
        name="Purchase Log Note Notifications",
        comodel_name="purchase.log.note.notify",
        inverse_name="purchase_order_type_id",
    )
    purchase_activity_notify_ids = fields.One2many(
        name="Purchase Activity Notifications",
        comodel_name="purchase.activity.notify",
        inverse_name="purchase_order_type_id",
    )

    def _get_purchase_notify_ids(self):
        return {
            "purchase_mail_notify_ids": self.purchase_mail_notify_ids,
            "purchase_log_note_notify_ids": self.purchase_log_note_notify_ids,
            "purchase_activity_notify_ids": self.purchase_activity_notify_ids,
        }
