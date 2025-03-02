/** @odoo-module */

import { CharField } from "@web/views/fields/char/char_field";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class UserNameCharField extends CharField {
    setup() {
        super.setup();
    }

    get emailDomain(){
        let email=this.props.record.data.email;
        return email ?email.split('@')[1]:''
    }
}

UserNameCharField.template = "owl_fields_widget.UserNameWidgetView";
UserNameCharField.components = { CharField};
UserNameCharField.supportedTypes = ["char"];


registry.category("fields").add("username", UserNameCharField);
