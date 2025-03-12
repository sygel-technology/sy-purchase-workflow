# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Create Related",
    "summary": "Create main-secondary relations beetween purchases with a wizard",
    "version": "17.0.1.0.0",
    "category": "Purchase",
    "website": "https://github.com/sygel-technology/sy-purchase-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "purchase",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/purchase_order_views.xml",
        "wizards/purchase_order_secondary_linker_views.xml",
    ],
}
