/** @odoo-module **/

import { registry } from '@web/core/registry';
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { getDefaultConfig } from "@web/views/view";

const { Component, useState, onWillStart, useRef,useSubEnv } = owl;

export class OwlDashboard extends Component {
    setup(){
        this.display={
            controlPanel:{"top-right":false,"bottom-right":false}
        }
        useSubEnv({
            config: {
                ...getDefaultConfig(),
                ...this.env.config,
            }
        });

        this.basicServicesPartnersServices=useService("basicServicesPartners");
        this.dashboardData=useState(this.basicServicesPartnersServices.dashboardData);
//        console.log(this.basicServicesPartners.dashboardData)

        this.simpleMailServices=useService("simpleMailService");
    }

    get owlBasicServices(){
        const owlBasicServices=this.env.services.basicServices;
        console.log(owlBasicServices);
        return owlBasicServices
    }

    openSimpleMailServices(){
        return this.simpleMailServices.open()
    }
}

OwlDashboard.template = 'owl_dashboard_create_services.OwlDashboardView'
OwlDashboard.components = {Layout}

registry.category('actions').add('owl_dashboard_create_services.action_odoo_dashboard_owl_js', OwlDashboard);