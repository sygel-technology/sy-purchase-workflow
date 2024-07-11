# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Purchase Order Line Display Number",
    "summary": "Configure the number of purchase order lines to be shown",
    "version": "15.0.1.0.0",
    "category": "Purchase",
    "website": "https://github.com/sygel-technology/sy-purchase-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "purchase",
    ],
    "data": ["data/purchase_order_line_display_number_data.xml"],
    "assets": {
        "web.assets_backend": [
            "purchase_order_line_display_number/static/src/js/form_view.js",
        ]
    },
}
