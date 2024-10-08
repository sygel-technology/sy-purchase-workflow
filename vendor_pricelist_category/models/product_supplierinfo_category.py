# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductSupplierinfoCategory(models.Model):
    _name = "product.supplierinfo.category"
    _description = "Product Supplierinfo Category"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = "complete_name"
    _order = "complete_name"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    complete_name = fields.Char(
        compute="_compute_complete_name",
        recursive=True,
        store=True,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Vendor",
        required=True,
        domain="[('company_id', 'in', [False, company_id])]",
        compute="_compute_partner_id",
        readonly=False,
        store=True,
        recursive=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
    description = fields.Text()
    parent_id = fields.Many2one(
        comodel_name="product.supplierinfo.category",
        ondelete="cascade",
        string="Parent Category",
        recursive=True,
    )
    child_id = fields.One2many(
        comodel_name="product.supplierinfo.category",
        inverse_name="parent_id",
        string="Child Categories",
    )
    parent_path = fields.Char(index=True, unaccent=False)
    use_discount_in_supplierinfo = fields.Boolean(
        compute="_compute_use_discount_in_supplierinfo",
        store=True,
        readonly=False,
        recursive=True,
    )
    use_different_parent_discount = fields.Boolean(
        compute="_compute_use_different_parent_discount",
        store=True,
        readonly=False,
        recursive=True,
    )
    discount = fields.Float(
        string="Discount (%)",
        digits="Discount",
        compute="_compute_discount",
        store=True,
        readonly=False,
        recursive=True,
    )

    @api.constrains("code", "company_id", "parent_id")
    def _check_code(self):
        for category in self.filtered("code"):
            categories_count = self.search_count(
                [
                    ("parent_id", "=", category.parent_id.id),
                    ("company_id", "=", category.company_id.id),
                    ("code", "=", category.code),
                ]
            )
            if categories_count > 1:
                raise ValidationError(
                    _(
                        "Code must be unique for categories with the same "
                        "parent category."
                    )
                )

    @api.constrains("parent_id")
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_("You cannot create recursive categories."))

    @api.constrains("partner_id")
    def _check_partner_id(self):
        for sel in self:
            if self.env["product.supplierinfo"].search(
                [
                    ("product_supplierinfo_category_id", "=", sel.id),
                    ("partner_id", "!=", sel.partner_id.id),
                ]
            ):
                raise ValidationError(
                    _(
                        "Vendor cannot be modified as this category has been used "
                        "in vendor pricelist with a different vendor."
                    )
                )

    @api.depends("parent_id", "parent_id.partner_id")
    def _compute_partner_id(self):
        for sel in self:
            partner_id = False
            if sel.parent_id:
                partner_id = sel.parent_id.partner_id.id
            sel.partner_id = partner_id

    @api.depends("parent_id", "parent_id.use_discount_in_supplierinfo")
    def _compute_use_discount_in_supplierinfo(self):
        for sel in self:
            use_discount_in_supplierinfo = False
            if sel.parent_id:
                use_discount_in_supplierinfo = (
                    sel.parent_id.use_discount_in_supplierinfo
                )
            sel.use_discount_in_supplierinfo = use_discount_in_supplierinfo

    @api.depends("parent_id", "parent_id.use_different_parent_discount")
    def _compute_use_different_parent_discount(self):
        for sel in self:
            use_different_parent_discount = False
            if sel.parent_id:
                use_different_parent_discount = (
                    sel.parent_id.use_different_parent_discount
                )
            sel.use_different_parent_discount = use_different_parent_discount

    @api.depends("use_different_parent_discount", "parent_id", "parent_id.discount")
    def _compute_discount(self):
        for sel in self:
            discount = 0.0
            if sel.parent_id and not sel.use_different_parent_discount:
                discount = sel.parent_id.discount
            sel.discount = discount

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = "{} / {}".format(
                    category.parent_id.complete_name,
                    category.name,
                )
            else:
                category.complete_name = category.name
