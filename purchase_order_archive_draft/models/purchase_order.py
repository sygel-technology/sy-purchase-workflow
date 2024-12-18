# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def toggle_active(self):
        if self.filtered(lambda po: po.state not in ["draft", "sent"] and po.active):
            raise UserError(_("Only 'Draft' or 'Sent' orders can be archived"))
        else:
            # Base definition of toggle_active
            active_recs = self.filtered(self._active_name)
            active_recs[self._active_name] = False
            (self - active_recs)[self._active_name] = True
