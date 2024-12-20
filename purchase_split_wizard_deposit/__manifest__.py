# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Split Wizard Deposit",
    "summary": "Split also purchase deposit invoices",
    "version": "16.0.1.0.0",
    "category": "Purchase",
    "website": "https://github.com/sygel-technology/sy-purchase-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "purchase_deposit",
        "purchase_split_wizard",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/purchase_views.xml",
        "wizards/purchase_split_wizard_views.xml",
    ],
}
