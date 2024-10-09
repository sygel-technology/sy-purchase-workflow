# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class PurchaseMailNotify(models.Model):
    _name = "purchase.mail.notify"
    _description = "Purchase Mail Notify"

    _inherit = ["mail.notify.mixin", "purchase.notify.mixin"]
