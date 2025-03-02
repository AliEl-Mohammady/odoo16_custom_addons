odoo.define('pos_clear_orderLines.ClearAllButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');
    const {_t} = require('web.core');

    class ClearAllButton extends PosComponent {
        setup() {
            super.setup();
            useListener('click', this.onClick);     //Event on click
        }

      async onClick() {
        const { confirmed } = await this.showPopup('ConfirmPopup', {
            title: _t('Confirmation Popup'),
            body: "Are you sure you want to clear all orders ?",
            confirmText: this.env._t('Yes'),
            cancelText: this.env._t('No'),
        });
        if (confirmed) {
//            console.log(">>>>>>>>>>",this.env.pos.get_order().orderlines.filter(line=>line.get_product()))
            var current_orderLines=this.env.pos.get_order();
            if (current_orderLines){
                current_orderLines.orderlines.filter(line=>line.get_product()).forEach(order_line=> current_orderLines.remove_orderline(order_line) )
            }
        }else{
            console.log("Confirmation Cancelled")
        }

      }

    }

    ClearAllButton.template = 'ClearAllButton';

    ProductScreen.addControlButton({
        component: ClearAllButton,
        position: ['before', 'OrderlineCustomerNoteButton'],
    });


    Registries.Component.add(ClearAllButton);

    return ClearAllButton;
});
