odoo.define('pos_orderLine.SetEmployeePopup', function(require) {
    'use strict';

    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const { _lt } = require('@web/core/l10n/translation');
    const { Gui } = require('point_of_sale.Gui');

    // formerly ErrorPopupWidget
    class SetEmployeePopup extends AbstractAwaitablePopup {
        setup() {
            super.setup();
            owl.onMounted(this.onMounted);
        }
        onMounted() {
            Gui.playSound('bell');
        }
    }
    SetEmployeePopup.template = 'SetEmployeePopup';

    SetEmployeePopup.defaultProps = {
        confirmText: _lt('Ok'),
        title: _lt('Error'),
        body: '',
        cancelKey: false,
    };

    Registries.Component.add(SetEmployeePopup);

    return SetEmployeePopup;
});
