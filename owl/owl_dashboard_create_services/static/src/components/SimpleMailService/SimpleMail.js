/** @odoo-module */

const { Component,useState } = owl

export class SimpleMail extends Component {
    setup(){

        this.state=useState({
            emailTo:"",
            subject:"",
            message:""
        })
    }
}


SimpleMail.template = "owl_dashboard_create_services.SimpleMail"


