/** @odoo-module */

import { registry } from "@web/core/registry"
import { SimpleMailContainer } from "./SimpleMailContainer"
const {reactive}=owl

export const simpleMailService = {
    dependencies: ["orm","user","rpc","notification"],
    async start(env, { orm,user,rpc,notification}) {

        const emailFrom=await orm.searchRead("res.partner",[["id","=",user.partnerId]])
        let simpleMail=reactive({
            isActive:false,
            emailFrom:emailFrom[0].email,
            open,
            close,
            send
        })

        registry.category('main_components').add('SimpleMailContainer', {
            Component: SimpleMailContainer,
            props:{simpleMail}
        });


        function open(){
            simpleMail.isActive=true
        }

        function close(){
            simpleMail.isActive=false
        }

        async function send(mail){
            console.log("Send Function",mail)
            const data={
                email_from:simpleMail.emailFrom,
                email_to:mail.emailTo,
                subject:mail.subject,
                message:mail.message
            }

            const newEmail=rpc('/owl/dashboard/simple_mail_service',data)
            if (newEmail){
                notification.add("Email Send notification",{
                    title: "Email Notification",
                    type: "info", //warning-danger
                })
            }else{
                notification.add("Email not Send ",{
                    title: "Email Notification",
                    type: "danger", //warning-danger
                })
            }

            close()
        }

        return {
            open
        }
    }
}



registry.category("services").add("simpleMailService", simpleMailService)