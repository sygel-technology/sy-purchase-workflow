# Copyright 2022 Angel Garcia de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Purchase internal product reference",
    "summary": "Shows the internal product reference or the supplier's reference in purchasing",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "website": "https://www.sygel.es",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'base',
        'product',
        'purchase',
    ],
    "data": [
        "views/res_config_settings_view.xml",
    ],
}
