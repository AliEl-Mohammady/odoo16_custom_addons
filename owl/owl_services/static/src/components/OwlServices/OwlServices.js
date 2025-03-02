/** @odoo-module **/

import { registry } from '@web/core/registry';
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { getDefaultConfig } from "@web/views/view";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { routeToUrl } from "@web/core/browser/router_service"
import { browser } from "@web/core/browser/browser"

const { Component, useState, onWillStart, useRef,useSubEnv } = owl;

export class OwlServices extends Component {
    setup(){
        this.notification = useService("notification");
        this.dialog = useService("dialog");
        this.effect = useService("effect");
        this.display={
            controlPanel:{"top-right":false,"bottom-right":false}
        }
        useSubEnv({
            config: {
                ...getDefaultConfig(),
                ...this.env.config,
            }
        });

        this.cookieServices = useService("cookie");
        console.log(this.cookieServices)
        if (!this.cookieServices.current.dark_mode){
            this.cookieServices.setCookie("dark_mode",false)
        }

        const router = this.env.services.router
        this.state=useState({
            dark_mode:this.cookieServices.current.dark_mode,
            get_http_data:[],
            post_http_data:[],
            rpc_data:[],
            orm_data:[],
            user_data:[],
            company_data:[],
            bg_success: router.current.search.bg_success,

        })

        const titleServices=useService("title");
        console.log(titleServices.getParts())
        titleServices.setParts({zopenerp:"Ali",odoo:"El-Mohammady",any:"OWL"})
    }

    showNotification(){
//        let notification=this.env.services.notification
        this.notification.add("owl notification services",{
                title: "Owl Notification",
                type: "info", //warning-danger
                message: this.env._t("Owl Test Notification"),
                sticky: false,
                className:"p-5",
                buttons: [{
                    name:"Notification Button",
                    onClick:()=>{
                        console.log("Hello from inside")
                    },
                    primary:true,
                },{
                    name:"Notification Again",
                    onClick:()=>{
                        this.showNotification()
                    },
                    primary:false,
                },]

            });
    }

    showDialog(){
        const dialog = this.env.services.dialog
        dialog.add(ConfirmationDialog, {
            title: "Dialog Service",
            body: "Are you sure you want to continue this action?",
            confirm: ()=>{
                this.showNotification()
            },
            cancel: ()=>{
                console.log("Dialog Cancelled")
            }
        }, {
            onClose: ()=> {
                console.log("Dialog service closed....")
            }
        })
        console.log(dialog)
    }

    showEffect(){
        console.log(this.effect)
        this.env.services.effect.add({
            type:"rainbow_man",
            message:"Welcome to our odoo services"
        })

    }

    cookieServicesFunc(){
        if(this.cookieServices.current.dark_mode == false){
            this.cookieServices.current.dark_mode=true;
        }else{
            this.cookieServices.current.dark_mode=false;
        }
        this.state.dark_mode=this.cookieServices.current.dark_mode;
        console.log(this.state.dark_mode)
//        this.cookieServices.deleteCookie("test")
    }

    async getHttpServices(){
        const http =this.env.services.http
        console.log(http)
        const get_http_data= await http.get('https://dummyjson.com/posts?sortBy=title&order=asc')
        this.state.get_http_data=get_http_data.posts
        console.log(this.state.get_http_data)
    }

    async postHttpServices(){
        const http =this.env.services.http
        console.log(http)
        const post_http_data= await http.post('https://dummyjson.com/posts/add',{userId:5,title:"Ali El-Mohammady"})
        this.state.post_http_data=post_http_data
        console.log(this.state.post_http_data)
    }

    async rpcServices(){
        const rpc =this.env.services.rpc
        const rpc_data= await rpc("/owl/rpc",{limit:10})
        this.state.rpc_data=rpc_data
        console.log(this.state.rpc_data)
    }

    async ormServices(){
        const orm =this.env.services.orm
        const orm_data= await orm.searchRead("res.partner",[],["id","name","email"])
        this.state.orm_data=orm_data
        console.log(this.state.orm_data)
    }

    actionServices(){
        const action =this.env.services.action
        action.doAction({
            type:"ir.actions.act_window",
            name:"Owl Action",
            res_model:"res.partner",
            domain:[["id",">",10]],
            context:{search_default_type_company:1},
            res_model:"res.partner",
            views:[[false,"list"],[false,"form"],[false,"kanban"]],
            view_mode:"list,form,kanban",
            target:"current",

        })
    }

    getRouterService(){
        const router = this.env.services.router
        console.log(router)
        let { search } = router.current
        search.bg_success = search.bg_success == "1" ? "0" : "1"
        console.log(router.current)
        browser.location.href = browser.location.origin + routeToUrl(router.current)
    }

    userServices(){
        const user=this.env.services.user
        console.log(user)
        this.state.user_data = JSON.stringify(user)
    }

    companyServices(){
        const company_data=this.env.services.company
        console.log(company_data)
        this.state.company_data = JSON.stringify(company_data)
    }

}

OwlServices.template = 'owl_services.OwlServicesView'
OwlServices.components = {Layout}

registry.category('actions').add('owl_services.action_odoo_services_owl_js', OwlServices);