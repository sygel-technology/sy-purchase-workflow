# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class PurchaseLogNoteNotify(models.Model):
    _name = "purchase.log.note.notify"
    _description = "Purchase Note Notify"

    _inherit = ["note.notify.mixin", "purchase.notify.mixin"]
