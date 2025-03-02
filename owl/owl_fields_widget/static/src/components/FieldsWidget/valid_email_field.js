/** @odoo-module */

import { registry } from "@web/core/registry"
import { EmailField } from "@web/views/fields/email/email_field"


class ValidEmailField extends EmailField {
    setup(){
        super.setup()
        console.log("This is res partner form widget")
    }

    get isValidEmail(){
        let re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return re.test(this.props.value)
    }
}

ValidEmailField.supportedTypes = ["char"];
ValidEmailField.template="owl_fields_widget.ResPartnerWidgetView"

registry.category("fields").add("valid_email", ValidEmailField);
