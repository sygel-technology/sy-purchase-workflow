# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Queued Purchase Notify",
    "summary": "Schedule email/logs/activities notificacions on purchases",
    "version": "17.0.1.0.0",
    "category": "Purchases",
    "website": "https://github.com/sygel-technology/sy-purchase-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base_queued_notify",
        "purchase_order_type",
    ],
    "data": [
        "security/queued_purchase_notify_security.xml",
        "security/ir.model.access.csv",
        "views/view_purchase_order_type_form.xml",
    ],
}
