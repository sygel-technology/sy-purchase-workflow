# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class SomethingCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_id = cls.env["res.partner"].create({"name": "Test partner"})
        cls.main_purchase_id = cls.env["purchase.order"].create(
            {"partner_id": cls.partner_id.id}
        )
        cls.secondary_purchase_id = cls.env["purchase.order"].create(
            {"partner_id": cls.partner_id.id, "can_be_secondary": True}
        )

    def test_create_secondary(self):
        wizard = (
            self.env["purchase.order.secondary.linker"]
            .with_context(**{"main_purchase_ids": self.main_purchase_id.ids})
            .create({"operation_type": "create"})
        )
        res = wizard.action_accept()
        purchase_id = self.env["purchase.order"].browse(res["res_id"])
        self.assertTrue(purchase_id)
        self.assertIn(purchase_id, self.main_purchase_id.secondary_purchase_ids)
        self.assertIn(self.main_purchase_id, purchase_id.main_purchase_ids)
        self.assertEqual(self.main_purchase_id.secondary_purchases_count, 1)
        self.assertEqual(purchase_id.main_purchases_count, 1)

    def test_link_secondary(self):
        wizard = (
            self.env["purchase.order.secondary.linker"]
            .with_context(**{"main_purchase_ids": self.main_purchase_id.ids})
            .create(
                {
                    "operation_type": "link",
                    "secondary_purchase_id": self.secondary_purchase_id.id,
                }
            )
        )
        wizard.action_accept()
        self.assertIn(
            self.secondary_purchase_id, self.main_purchase_id.secondary_purchase_ids
        )
        self.assertIn(
            self.main_purchase_id, self.secondary_purchase_id.main_purchase_ids
        )
        self.assertEqual(self.main_purchase_id.secondary_purchases_count, 1)
        self.assertEqual(self.secondary_purchase_id.main_purchases_count, 1)
