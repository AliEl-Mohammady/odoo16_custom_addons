/** @odoo-module */
import { SimpleMail } from "./SimpleMail"
const { Component, xml,useState } = owl;

export class SimpleMailContainer extends Component {
    setup(){
        this.state=useState(this.props.simpleMail)
    }
}

SimpleMailContainer.template = xml`
    <div class="o_simple_mail_manager">
        <t t-if="state.isActive==true">
            <SimpleMail t-props="state"/>
        </t>
    </div>
`
SimpleMailContainer.components={SimpleMail}

