# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import Form, TransactionCase


class TestPurchaseSplitWizard(TransactionCase):
    def setUp(self):
        super().setUp()

        self.partner = self.env["res.partner"].create({"name": "Test Partner"})
        self.product1 = self.env["product.product"].create(
            {
                "name": "Product 1",
                "standard_price": 100.0,
                "list_price": 80.0,
                "type": "service",
            }
        )
        self.product2 = self.env["product.product"].create(
            {
                "name": "Product2",
                "standard_price": 200.0,
                "list_price": 180.0,
                "type": "service",
            }
        )
        self.purchase_id = self.env["purchase.order"].create(
            {
                "partner_id": self.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product1.id,
                            "name": f"{self.product1.name}",
                            "product_qty": 20.0,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": self.product2.id,
                            "name": f"{self.product2.name}",
                            "product_qty": 10.0,
                        },
                    ),
                ],
            }
        )

    def test_partially_split(self):
        """
        Partially split the purchase.
        Assert Values
        """
        purchase_split_wizard = Form(
            self.env["purchase.split.wizard"].with_context(
                default_purchase_origin_id=self.purchase_id.id
            )
        )
        purchase_split_wizard.partner_ref = "Test"
        with purchase_split_wizard.wizard_line_ids.edit(0) as line:
            line.product_qty = 10
        with purchase_split_wizard.wizard_line_ids.edit(1) as line:
            line.product_qty = 10
        purchase_split = purchase_split_wizard.save()
        res = purchase_split.action_accept()
        new_purchase = self.env["purchase.order"].browse(res["res_id"])
        self.assertEqual(new_purchase.partner_ref, "Test")
        self.assertEqual(new_purchase.order_line[0].product_qty, 10)
        self.assertEqual(new_purchase.order_line[1].product_qty, 10)
        self.assertEqual(new_purchase.split_status, "children")
        self.assertEqual(self.purchase_id.split_status, "parent_partially")

    def test_complete_split(self):
        """
        Totally split the purchase.
        Assert Values
        Cancel splitted children.
        Assert Values
        """
        purchase_split_wizard = Form(
            self.env["purchase.split.wizard"].with_context(
                default_purchase_origin_id=self.purchase_id.id
            )
        )
        purchase_split_wizard.partner_ref = "Test"
        with purchase_split_wizard.wizard_line_ids.edit(0) as line:
            line.product_qty = 20
        with purchase_split_wizard.wizard_line_ids.edit(1) as line:
            line.product_qty = 10
        purchase_split = purchase_split_wizard.save()
        res = purchase_split.action_accept()
        new_purchase = self.env["purchase.order"].browse(res["res_id"])

        self.assertEqual(new_purchase.partner_ref, "Test")
        self.assertEqual(new_purchase.order_line[0].product_qty, 20)
        self.assertEqual(new_purchase.order_line[1].product_qty, 10)
        self.assertEqual(new_purchase.split_status, "children")

        new_purchase.write({"state": "cancel"})
        new_purchase.unlink()
        self.assertEqual(self.purchase_id.split_status, "none")

    def test_partially_with_notes(self):
        """
        Add a note
        Partially split the purchase.
        Assert Values
        """
        self.purchase_id.write(
            {
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "display_type": "line_section",
                            "name": "haha i will break your test",
                            "product_qty": 0.0,
                        },
                    ),
                ]
            }
        )

        purchase_split_wizard = Form(
            self.env["purchase.split.wizard"].with_context(
                default_purchase_origin_id=self.purchase_id.id
            )
        )
        purchase_split = purchase_split_wizard.save()
        res = purchase_split.action_accept()
        new_purchase = self.env["purchase.order"].browse(res["res_id"])

        self.assertEqual(len(new_purchase.order_line), 1)
        self.assertEqual(new_purchase.order_line.display_type, "line_section")
