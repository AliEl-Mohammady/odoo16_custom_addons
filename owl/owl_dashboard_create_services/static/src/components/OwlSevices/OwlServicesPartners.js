/** @odoo-module **/

import { registry } from '@web/core/registry';
const {reactive}=owl

export const owlBasicServicesPartners={
    dependencies: ["rpc"],
    async start(env, { rpc }) {
        let dashboardData=reactive({})
        Object.assign(dashboardData,await rpc("/owl/dashboard/rpc"));

//        let dashboardData=await rpc("/owl/dashboard/rpc");
        setInterval(async () => {
            Object.assign(dashboardData,await rpc("/owl/dashboard/rpc"));
//            console.log("dashboardDataset",dashboardData);
        },3000)

        return{
            dashboardData
        }
    }

}


registry.category('services').add('basicServicesPartners', owlBasicServicesPartners);
