# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    product_supplierinfo_category_id = fields.Many2one(
        comodel_name="product.supplierinfo.category",
        string="Category",
        domain="[('partner_id', '=', partner_id)]",
    )
    use_category_discount = fields.Boolean(
        related="product_supplierinfo_category_id.use_discount_in_supplierinfo",
    )

    @api.depends(
        "partner_id",
        "product_supplierinfo_category_id",
        "product_supplierinfo_category_id.use_discount_in_supplierinfo",
        "product_supplierinfo_category_id.discount",
    )
    def _compute_discount(self):
        ret_val = super()._compute_discount()
        for sel in self.filtered(
            lambda a: a.product_supplierinfo_category_id
            and a.product_supplierinfo_category_id.use_discount_in_supplierinfo
        ):
            sel.discount = sel.product_supplierinfo_category_id.discount
        return ret_val
