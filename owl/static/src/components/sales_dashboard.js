/** @odoo-module **/

import { registry } from "@web/core/registry";
import { KpiCard } from "./kpi_card/kpi_card";
import { ChartRenderer } from "./chart_renderer/chart_renderer";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
const { Component, onWillStart, useRef,onMounted,useState} = owl
//onMounted:when it is appear
//onWillunamounted:when it is disappear
//useState:when it is used

export class OwlSalesDashboard extends Component {
        getTopProducts(){
            this.state.topProducts={}
        };
        getTopSalesPeople(){
            this.state.topSalesPeople={}
        };
        getMonthlySales(){
            this.state.monthlySales={}
        };
        getPartnerOrder(){
            this.state.partnerOrder={}
        };
        setup(){
           this.state = useState({
               quotation:{
                    value:10,
                    percentage:6
               }
           })
           this.orm=useService("orm")
           this.actionServer=useService("action")

           onWillStart(async()=>{
                this.getDates()
                await this.getQuotations()
                await this.getOrders()
           })
        };

        async onChangePeriod(){
            this.getDates()
            await this.getQuotations()
            await this.getOrders()
        }

        getDates(){
            this.state.current_date=moment().subtract(this.state.period,'days').format('L');
            this.state.previous_date=moment().subtract(this.state.period * 2,'days').format('L');
        }

        async getQuotations(){
            let domain=[["state","in",["draft","sent"]]]
            if (this.state.period>0){
                domain.push(["date_order",">",this.state.current_date])
            }
            const data=await this.orm.searchCount("sale.order",domain)
            this.state.quotation.value=data

            //previous domain
            let prev_domain=[["state","in",["draft","sent"]]]
            if (this.state.period>0){
                prev_domain.push(["date_order",">",this.state.previous_date],["date_order","<=",this.state.current_date])
            }

            const prev_data=await this.orm.searchCount("sale.order",prev_domain)
            const percentage=((data-prev_data)/prev_data)*100
            this.state.quotation.percentage=percentage.toFixed(2)
        }
        async getOrders(){
            let domain=[["state","in",["sale","done"]]]
            if (this.state.period>0){
                domain.push(["date_order",">",this.state.current_date])
            }
            const data=await this.orm.searchCount("sale.order",domain)
//            this.state.quotation.value=data

            //previous domain
            let prev_domain=[["state","in",["sale","done"]]]
            if (this.state.period>0){
                prev_domain.push(["date_order",">",this.state.previous_date],["date_order","<=",this.state.current_date])
            }

            const prev_data=await this.orm.searchCount("sale.order",prev_domain)
            const percentage=((data-prev_data)/prev_data)*100
//            this.state.quotation.percentage=percentage.toFixed(2)

            //revenue
            const current_revenue=await this.orm.readGroup("sale.order",domain,["amount_total:sum"],[])
            const prev_revenue=await this.orm.readGroup("sale.order",prev_domain,["amount_total:sum"],[])
            const revenue_percentage=((current_revenue[0].amount_total-prev_revenue[0].amount_total)/prev_revenue[0].amount_total)*100

            //Average
            const current_average=await this.orm.readGroup("sale.order",domain,["amount_total:avg"],[])
            const prev_average=await this.orm.readGroup("sale.order",prev_domain,["amount_total:avg"],[])
            const average_percentage=((current_average[0].amount_total-prev_average[0].amount_total)/prev_average[0].amount_total)*100

            this.state.orders ={
                value:data,
                percentage :percentage.toFixed(2),
                revenue:`$${((current_revenue[0].amount_total)/1000).toFixed(2)}K`,
                revenue_percentage:revenue_percentage.toFixed(2),
                average:`$${((current_average[0].amount_total)/1000).toFixed(2)}K`,
                average_percentage:average_percentage.toFixed(2),
            }
        }

//        viewQuotations(){
//            this.actionServer.doAction("sale.action_quotations_with_onboarding",{
//                additionalContext : {
//                    search_default_draft:1,
//                    search_default_my_quotation:2,
//                }
//            })
//        }
        async viewQuotations(){
            let domain=[["state","in",["draft","sent"]]]
            if (this.state.period>0){
                domain.push(["date_order",">",this.state.current_date])
            }

            let list_view=await this.orm.searchRead("ir.model.data",[["name","=","view_quotation_tree_with_onboarding"]],["res_id"])

            this.actionServer.doAction({
                type:"ir.actions.act_window",
                name:"Quotations",
                res_model:"sale.order",
                domain,
                views:[
                    [list_view.length>0?list_view[0].res_id:false,"list"],
                    [false,"form"],
                ],
            })
        }

        viewOrders(){
            let domain=[["state","in",["done","sale"]]]
            if (this.state.period>0){
                domain.push(["date_order",">",this.state.current_date])
            }

            this.actionServer.doAction({
                type:"ir.actions.act_window",
                name:"Orders",
                res_model:"sale.order",
                domain,
                context:{group_by:["date_order"]},
                views:[
                    [false,"list"],
                    [false,"form"],
                ],
            })
        }

        revenuesOrder(){
            let domain=[["state","in",["done","sale"]]]
            if (this.state.period>0){
                domain.push(["date_order",">",this.state.current_date])
            }

            this.actionServer.doAction({
                type:"ir.actions.act_window",
                name:"Revenues",
                res_model:"sale.order",
                domain,
                views:[
                    [false,"pivot"],
                    [false,"form"],
                ],
            })
        }

        averageOrder(){
            let domain=[["state","in",["done","sale"]]]
            if (this.state.period>0){
                domain.push(["date_order",">",this.state.current_date])
            }

            this.actionServer.doAction({
                type:"ir.actions.act_window",
                name:"Average",
                res_model:"sale.order",
                domain,
                views:[
                    [false,"graph"],
                    [false,"form"],
                ],
            })
        }

}
//create class

OwlSalesDashboard.template="owl.OwlSalesDashboard"
OwlSalesDashboard.components={ KpiCard, ChartRenderer }

registry.category("actions").add("owl.sales_dashboard", OwlSalesDashboard);
//registry.category("actions").add("tag_field in action", class name);
