# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Create Manual Incomming",
    "summary": "Add manual stock receipt creation to purchase order",
    "version": "16.0.1.0.0",
    "category": "Purchase",
    "website": "https://github.com/sygel-technology/sy-purchase-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "purchase_split_wizard",
    ],
    "data": [
        "views/purchase_order_views.xml",
    ],
}
