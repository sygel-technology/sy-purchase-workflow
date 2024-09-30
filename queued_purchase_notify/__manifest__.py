# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Queued Purchase Notify",
    "summary": "Send email/logs/activities notificacions from purchases",
    "version": "12.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://github.com/sygel-technology/sy-purchase-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "queue_job",
        "purchase_order_type",
        "purchase_picking_notify_interface",
    ],
    "data": [
        "views/view_purchase_order_type_form.xml",
        "views/purchase_order_view.xml",
        "security/queued_purchase_notify_security.xml",
        "security/ir.model.access.csv",
    ],
}
