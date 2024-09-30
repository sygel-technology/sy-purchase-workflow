# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime
from datetime import timedelta

from odoo import api, fields, models

from odoo.addons.queue_job.job import DONE, job


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    purchase_queue_ids = fields.Many2many(
        string="Purchase Queues",
        comodel_name="queue.job",
        compute="_compute_purchase_queues",
    )
    has_queues = fields.Boolean(
        string="Has Queues", readonly=True, compute="_compute_has_queues"
    )

    @api.multi
    def _compute_purchase_queues(self):
        for sel in self:
            all_queues = self.env["queue.job"].search(
                [
                    ("model_name", "=", "purchase.order"),
                ]
            )
            sel.purchase_queue_ids = all_queues.filtered(
                lambda a: sel.id in a.record_ids
            ).ids

    @api.depends("purchase_queue_ids")
    def _compute_has_queues(self):
        for sel in self:
            sel.has_queues = True if sel.purchase_queue_ids else False

    @api.multi
    def write(self, values):
        return_value = super(PurchaseOrder, self).write(values)
        # no se hace el for sel in self porque en el super tampoc se hace
        for sel in self:
            if (sel.partner_ref and sel.partner_ref != "") or (
                values.get("partner_ref") and values.get("partner_ref") != ""
            ):
                sel.set_queues_to_done("Set to done when reference was selected")
        return return_value

    @api.multi
    def button_confirm(self):
        return_value = super(PurchaseOrder, self).button_confirm()
        for sel in self.filtered(lambda a: not a.partner_ref or a.partner_ref == ""):
            sel.purchase_notify()
        return return_value

    @api.multi
    def button_cancel(self):
        super(PurchaseOrder, self).button_cancel()
        for sel in self:
            sel.set_queues_to_done("Set to done when PO was cancelled")

    def purchase_notify(self):
        order_type = self.order_type
        for mail in order_type.purchase_mail_notify_ids:
            self.with_delay(
                eta=int(mail.time_after_confirmation * 3600)
            ).delay_purchase_mail_notify(mail)
        for log in order_type.purchase_log_note_notify_ids:
            self.with_delay(
                eta=int(log.time_after_confirmation * 3600)
            ).delay_purchase_log_notify(log)
        for activity in order_type.purchase_activity_notify_ids:
            self.with_delay(
                eta=int(activity.time_after_confirmation * 3600)
            ).delay_purchase_activity_notify(activity)

    @job(default_channel="root.purchase_notify")
    def delay_purchase_mail_notify(self, mail):
        if not self.partner_ref or self.partner_ref == "":
            self.message_post_with_template(mail.mail_template_id.id)

    @job(default_channel="root.purchase_notify")
    def delay_purchase_log_notify(self, log):
        if not self.partner_ref or self.partner_ref == "":
            self.env["mail.message"].create(
                {
                    "body": log.note_text,
                    "model": "purchase.order",
                    "res_id": self.id,
                    "message_type": "comment",
                    "subtype_id": self.env.ref("mail.mt_note").id,
                }
            )

    @job(default_channel="root.purchase_notify")
    def delay_purchase_activity_notify(self, activity):
        if (not self.partner_ref or self.partner_ref == "") and self.user_id:
            deadline = fields.Datetime.to_string(
                datetime.datetime.now() + timedelta(days=activity.time_to_deadline)
            )
            self.env["mail.activity"].create(
                {
                    "activity_type_id": self.env.ref("mail.mail_activity_data_todo").id,
                    "date_deadline": deadline,
                    "summary": activity.summary,
                    "note": activity.note,
                    "user_id": activity.user_id.id,
                    "res_id": self.id,
                    "res_model_id": self.env["ir.model"]
                    .search([("model", "=", "purchase.order")], limit=1)
                    .id,
                }
            )

    def set_queues_to_done(self, message):
        for notification in self.purchase_queue_ids.filtered(
            lambda a: a.state not in ["done"]
        ):
            notification._change_job_state(DONE, message)
