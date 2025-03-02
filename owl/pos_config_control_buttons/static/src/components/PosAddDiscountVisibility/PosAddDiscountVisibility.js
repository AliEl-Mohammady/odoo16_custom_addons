/** @odoo-module */

import Registries from "point_of_sale.Registries";
import { PosGlobalState } from "point_of_sale.models";

const PosControlButton = (PosGlobalState) => class PosControlButton extends PosGlobalState {
    async _processData(loadedData) {
        await super._processData(...arguments);
        this.visible_discount_control = loadedData['visible_discount_control'];
    }
}
Registries.Model.extend(PosGlobalState, PosControlButton);

