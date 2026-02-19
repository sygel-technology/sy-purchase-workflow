# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tests.common import TransactionCase


class TestPurchaseProductInternalReference(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.env.company.internal_ref_product = True
        cls.vendor = cls.env["res.partner"].create(
            {
                "name": "Test Vendor",
                "supplier_rank": 1,
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "default_code": "INT001",
                "type": "consu",
            }
        )
        cls.env["product.supplierinfo"].create(
            {
                "partner_id": cls.vendor.id,
                "product_tmpl_id": cls.product.product_tmpl_id.id,
                "product_code": "SUP001",
            }
        )

    def test_force_internal_reference(self):
        """
        When the setting is enabled, the product display name
        must always show the internal reference,
        even if a supplier reference exists.
        """
        product = self.product.with_context(partner_id=self.vendor.id)
        display = product.display_name
        self.assertIn(
            "INT001",
            display,
            "Internal reference should be displayed when setting is enabled.",
        )
        self.assertNotIn(
            "SUP001",
            display,
            "Supplier reference should not be displayed when setting is enabled.",
        )

    def test_standard_behavior_without_setting(self):
        """
        When the setting is disabled, the standard behavior
        should apply and the supplier reference must be shown.
        """
        self.env.company.internal_ref_product = False
        product = self.product.with_context(partner_id=self.vendor.id)
        display = product.display_name
        self.assertIn(
            "SUP001",
            display,
            "Supplier reference should be displayed when setting is disabled.",
        )

    def test_get_product_purchase_description(self):
        """
        In purchase orders, when the setting is enabled,
        the internal reference must be used in the line description.
        """
        purchase = self.env["purchase.order"].create(
            {
                "partner_id": self.vendor.id,
            }
        )
        line = self.env["purchase.order.line"].create(
            {
                "order_id": purchase.id,
                "product_id": self.product.id,
                "name": "Temp",
                "product_qty": 1.0,
                "product_uom": self.product.uom_po_id.id,
                "price_unit": 10.0,
                "date_planned": fields.Datetime.now(),
            }
        )
        product_lang = self.product.with_context(
            partner_id=self.vendor.id,
        )
        description = line._get_product_purchase_description(product_lang)
        self.assertIn(
            "INT001",
            description,
            "Internal reference should be used in purchase line description"
            " when setting is enabled.",
        )
        self.assertNotIn(
            "SUP001",
            description,
            "Supplier reference should not appear in purchase line description "
            " when setting is enabled.",
        )
