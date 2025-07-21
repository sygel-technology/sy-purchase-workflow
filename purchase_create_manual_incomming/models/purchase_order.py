# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, exceptions
from odoo import SUPERUSER_ID


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _create_picking_force(self):
        StockPicking = self.env['stock.picking']
        for order in self:
            if any(product.type in ['product', 'consu'] for product in order.order_line.product_id):
                order = order.with_company(order.company_id)
                pickings = order.picking_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
                if not pickings:
                    res = order._prepare_picking()
                    picking = StockPicking.with_user(SUPERUSER_ID).create(res)
                    pickings = picking
                else:
                    picking = pickings[0]
                moves = order.order_line._create_stock_moves(picking)
                moves = moves.filtered(lambda x: x.state not in ('done', 'cancel'))._action_confirm()
                seq = 0
                for move in sorted(moves, key=lambda move: move.date):
                    seq += 5
                    move.sequence = seq
                moves._action_assign()
                forward_pickings = self.env['stock.picking']._get_impacted_pickings(moves)
                (pickings | forward_pickings).action_confirm()
                picking.message_post_with_view('mail.message_origin_link',
                    values={'self': picking, 'origin': order},
                    subtype_id=self.env.ref('mail.mt_note').id)
        return True

    def action_confirm_create_picking_force(self):
        self.ensure_one()
        if self.split_status == 'children':
            raise exceptions.UserError('Manual receipt cannot be created for sub-purchases.')

        self._create_picking_force()

        picking = self.picking_ids.filtered(lambda p: p.state not in ('done', 'cancel'))
        if picking:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'stock.picking',
                'res_id': picking[0].id,
                'view_mode': 'form',
                'target': 'current',
            }
        return True
