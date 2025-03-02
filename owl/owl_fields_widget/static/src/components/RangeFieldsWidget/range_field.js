/** @odoo-module **/

import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { Component, useState, onWillUpdateProps } from "@odoo/owl";

export class RangeField extends Component {
    setup() {
        this.state = useState({
            range: this.props.value || '',
        });
        console.log(this.props);
        const {currency_id}=this.props.record.data;
        this.currency_id =currency_id || '';
    }}

RangeField.template = "owl_fields_widget.RangeField";
RangeField.props = {
    ...standardFieldProps,
};

RangeField.supportedTypes = ["integer"];
registry.category("fields").add("range", RangeField);
