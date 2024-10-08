# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError, ValidationError
from odoo.tests import Form, common


class TestVendorPricelistCategory(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.vendor = cls.env["res.partner"].create({"name": "Test Vendor"})
        cls.vendor_alt = cls.env["res.partner"].create({"name": "Test Vendor Alt"})
        cls.product = cls.env["product.template"].create(
            {
                "name": "Test Product",
                "list_price": 100.0,
            }
        )

    def test_supplierinfo_discount(self):
        supplierinfo_category = self.env["product.supplierinfo.category"].create(
            {
                "name": "Supplierinfo Category",
                "code": "A",
                "partner_id": self.vendor.id,
                "use_discount_in_supplierinfo": True,
                "discount": 25.0,
            }
        )
        vendor_pricelist = self.env["product.supplierinfo"].create(
            {
                "partner_id": self.vendor.id,
                "product_tmpl_id": self.product.id,
                "discount": 10.0,
            }
        )
        self.assertFalse(vendor_pricelist.use_category_discount)
        self.assertEqual(vendor_pricelist.discount, 10.0)

        # Assign category to pricelist
        vendor_pricelist.write(
            {"product_supplierinfo_category_id": supplierinfo_category.id}
        )
        self.assertTrue(vendor_pricelist.use_category_discount)
        self.assertEqual(vendor_pricelist.discount, supplierinfo_category.discount)

        # Create a subcategory
        supplierinfo_form = Form(self.env["product.supplierinfo.category"])
        supplierinfo_form.name = "Supplierinfo Subcategory"
        supplierinfo_form.code = "B"
        supplierinfo_form.parent_id = supplierinfo_category
        supplierinfo_subcategory = supplierinfo_form.save()
        self.assertTrue(supplierinfo_subcategory.use_discount_in_supplierinfo)
        self.assertEqual(
            supplierinfo_subcategory.partner_id, supplierinfo_category.partner_id
        )
        self.assertEqual(
            supplierinfo_subcategory.discount, supplierinfo_category.discount
        )

        # Use a different discount in subcategory to the one used in the parent category
        supplierinfo_subcategory.write({"use_different_parent_discount": True})
        self.assertEqual(supplierinfo_subcategory.discount, 0.0)

        # Assign the subcategory to the pricelist
        vendor_pricelist.write(
            {"product_supplierinfo_category_id": supplierinfo_subcategory.id}
        )
        self.assertEqual(vendor_pricelist.discount, supplierinfo_subcategory.discount)

        # Modify the discount applied by the subcategory
        supplierinfo_subcategory.write({"discount": 30.0})
        self.assertEqual(vendor_pricelist.discount, 30.0)

    def test_supplierinfo_category_recursion(self):
        supplierinfo_category_a = self.env["product.supplierinfo.category"].create(
            {
                "name": "Supplierinfo Category A",
                "code": "A",
                "partner_id": self.vendor.id,
            }
        )
        supplierinfo_category_b = self.env["product.supplierinfo.category"].create(
            {
                "name": "Supplierinfo Category B",
                "code": "B",
                "partner_id": self.vendor.id,
                "parent_id": supplierinfo_category_a.id,
            }
        )
        # Avoid recursion
        with self.assertRaises(UserError):
            supplierinfo_category_a.write({"parent_id": supplierinfo_category_b.id})

    def test_check_partner(self):
        supplierinfo_category = self.env["product.supplierinfo.category"].create(
            {"name": "Supplierinfo Category", "code": "A", "partner_id": self.vendor.id}
        )
        self.env["product.supplierinfo"].create(
            {
                "partner_id": self.vendor.id,
                "product_tmpl_id": self.product.id,
                "discount": 10.0,
                "product_supplierinfo_category_id": supplierinfo_category.id,
            }
        )
        # Make sure the vendor in the category is not different to the vendor
        # to which the category is applied
        with self.assertRaises(ValidationError):
            supplierinfo_category.write({"partner_id": self.vendor_alt.id})

    def test_check_supplier_category_code(self):
        # Right code: Different code
        supplierinfo_category_a = self.env["product.supplierinfo.category"].create(
            {
                "name": "Supplierinfo Category-A",
                "code": "A",
                "partner_id": self.vendor.id,
            }
        )
        supplierinfo_category_b = self.env["product.supplierinfo.category"].create(
            {
                "name": "Supplierinfo Category-B",
                "code": "B",
                "partner_id": self.vendor.id,
            }
        )
        self.assertTrue(supplierinfo_category_a)
        self.assertEqual(supplierinfo_category_a.code, "A")
        self.assertTrue(supplierinfo_category_b)
        self.assertEqual(supplierinfo_category_b.code, "B")

        # Wrong code: Same code in same level (no parent_id)
        with self.assertRaises(ValidationError):
            self.env["product.supplierinfo.category"].create(
                {
                    "name": "Supplierinfo Category-C",
                    "code": "A",
                    "partner_id": self.vendor.id,
                }
            )

        # Right code: Same code in different level
        supplierinfo_category_a_a = self.env["product.supplierinfo.category"].create(
            {
                "name": "Supplierinfo Category-A-A",
                "code": "A",
                "partner_id": self.vendor.id,
                "parent_id": supplierinfo_category_a.id,
            }
        )
        self.assertTrue(supplierinfo_category_a_a)
        self.assertEqual(supplierinfo_category_a.code, supplierinfo_category_a_a.code)

        # Wrong code: Same code in same level (with parent_id)
        with self.assertRaises(ValidationError):
            self.env["product.supplierinfo.category"].create(
                {
                    "name": "Supplierinfo Category-C-B",
                    "code": "A",
                    "partner_id": self.vendor.id,
                    "parent_id": supplierinfo_category_a.id,
                }
            )
