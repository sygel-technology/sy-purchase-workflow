# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import Form

from odoo.addons.purchase_split_wizard.tests.test_purchase_split_wizard import (
    TestPurchaseSplitWizard,
)


class TestPurchaseSplitWizardDeposit(TestPurchaseSplitWizard):
    def setUp(self):
        super().setUp()
        product = (
            self.env["product.product"]
            .sudo()
            .create(
                {
                    "name": "Purchase Deposit",
                    "type": "service",
                    "purchase_method": "purchase",
                }
            )
        )
        self.env.company.sudo().purchase_deposit_product_id = product

    def create_advance_payment_form(self):
        ctx = {
            "active_id": self.purchase_id.id,
            "active_ids": [self.purchase_id.id],
            "active_model": "purchase.order",
            "create_bills": True,
        }
        CreateDeposit = self.env["purchase.advance.payment.inv"]
        advance_form = Form(CreateDeposit.with_context(**ctx))
        return advance_form

    def test_deposit_split(self):
        f = self.create_advance_payment_form()
        f.advance_payment_method = "fixed"
        f.amount = 2
        wizard = f.save()
        wizard.create_invoices()
        purchase_split_wizard = Form(
            self.env["purchase.split.wizard"].with_context(
                default_purchase_origin_id=self.purchase_id.id
            )
        )
        self.assertTrue(purchase_split_wizard.split_advances)
        self.assertTrue(purchase_split_wizard.advance_line_ids)
        with purchase_split_wizard.advance_line_ids.edit(1) as line:
            line.amount = 2
        purchase_split = purchase_split_wizard.save()
        res = purchase_split.action_accept()
        new_purchase = self.env["purchase.order"].browse(res["res_id"])
        new_deposit_line = new_purchase.order_line.filtered(
            lambda li: (li.is_deposit and not li.display_type)
        )
        self.assertTrue(new_deposit_line)
        self.assertEqual(new_deposit_line.price_unit, 2)
