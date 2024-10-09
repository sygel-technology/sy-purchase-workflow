# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class PurchaseActivityNotify(models.Model):
    _name = "purchase.activity.notify"
    _description = "Purchase Mail Notify"

    _inherit = ["activity.notify.mixin", "purchase.notify.mixin"]
