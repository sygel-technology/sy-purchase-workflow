# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        res = super().button_confirm()
        notity_set = self.order_type._get_purchase_notify_ids()
        for notify_ids in notity_set.values():
            for notify_id in notify_ids:
                for rec in self:
                    if notify_id.is_to_notify(rec):
                        notify_id.notify(rec)
        return res
