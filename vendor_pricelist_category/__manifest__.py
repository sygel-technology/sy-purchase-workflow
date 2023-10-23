# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Vendor Pricelist Category",
    "summary": "Categorize vendor pricelists",
    "version": "16.0.1.0.0",
    "category": "Purchase",
    "website": "https://www.sygel.es",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "purchase_triple_discount"
    ],    
    "data": [
        "security/ir.model.access.csv",
        "views/product_supplierinfo_category_view.xml",
        "views/product_supplierinfo_views.xml"
    ],
}
