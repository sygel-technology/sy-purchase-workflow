/* Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
 *  * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define(
    "purchase_order_line_display_number.purchase_order_line_display_number",
    function (require) {
        "use strict";
        var FormView = require("web.FormView");
        var rpc = require("web.rpc");

        FormView.include({
            _setSubViewLimit: function (attrs) {
                this._super(attrs);
                if (
                    this.modelParams.modelName === "purchase.order" &&
                    this.fieldsView.name === "purchase.order.form"
                ) {
                    const limit = rpc
                        .query({
                            model: "ir.config_parameter",
                            method: "get_param",
                            args: ["purchase_order_line_display_number.number"],
                        })
                        .then((res) => {
                            if (!_.isUndefined(res)) {
                                attrs.limit = parseInt(res);
                            }
                        });
                }
            },
        });
    }
);
