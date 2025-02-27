# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestPurchaseOrderNoPrice(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_id = cls.env["res.partner"].create({"name": "Test partner"})
        cls.product_price = 10.0
        cls.product_id = cls.env["product.product"].create(
            {"name": "Test product", "standard_price": cls.product_price}
        )
        cls.purchase_id = cls.env["purchase.order"].create(
            {"partner_id": cls.partner_id.id}
        )

    def _purchase_add_line(self, purchase, quantity):
        purchase.write(
            {
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_id.id,
                            "product_uom": self.product_id.uom_id.id,
                            "name": self.product_id.name,
                            "product_qty": quantity,
                        },
                    )
                ],
            }
        )

    def test_zero_price(self):
        self._purchase_add_line(self.purchase_id, 1)
        self.assertEqual(self.purchase_id.order_line[0].price_unit, self.product_price)

        self.partner_id.zero_purchase_price = True
        self._purchase_add_line(self.purchase_id, 1)
        self.assertEqual(self.purchase_id.order_line[1].price_unit, 0.0)
