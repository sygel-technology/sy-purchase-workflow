# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Split Wizard Order Type",
    "summary": "Purchase Split Wizard with order type field",
    "version": "16.0.1.0.0",
    "category": "Purchase",
    "website": "https://github.com/sygel-technology/sy-purchase-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "purchase_split_wizard",
        "purchase_order_type",
    ],
    "data": [
        "wizards/purchase_split_wizard_views.xml",
    ],
}
