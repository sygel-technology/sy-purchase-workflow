# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Split Wizard",
    "summary": "Wizard to split purchase orders into multiple ones",
    "version": "16.0.1.1.0",
    "category": "Purchase",
    "website": "https://github.com/sygel-technology/sy-purchase-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "account_payment_purchase",
        "purchase_order_archive_draft",
        "purchase_stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/purchase_order_views.xml",
        "wizards/purchase_split_wizard_views.xml",
    ],
}
