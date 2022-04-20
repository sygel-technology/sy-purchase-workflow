# Copyright 2022 Angel Garcia de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    internal_ref_product = fields.Boolean(
        string="Show internal product reference",
        help="Show the internal product reference on purchases. The default is the supplier's reference.",
        default=False,
    )
