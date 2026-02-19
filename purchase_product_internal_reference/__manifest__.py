# Copyright 2022 Angel Garcia de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Purchase product internal reference",
    "summary": "Display internal product reference in purchase orders",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "website": "https://github.com/sygel-technology/sy-purchase-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "product",
        "purchase",
    ],
    "data": [
        "views/res_config_settings_view.xml",
    ],
}
