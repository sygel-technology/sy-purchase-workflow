# Copyright 2022 Angel Garcia de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    internal_ref_product = fields.Boolean(
        related="company_id.internal_ref_product",
        string="Show internal product reference",
        help="Show the internal product reference on purchases. The default is the supplier's reference.",
        store=True,
        readonly=False,
    )
