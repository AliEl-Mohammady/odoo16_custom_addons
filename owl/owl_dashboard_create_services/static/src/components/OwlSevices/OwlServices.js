/** @odoo-module **/

import { registry } from '@web/core/registry';
const{markup}=owl;

export const owlBasicServices={
    start(){
        function normalFunction(){
            console.log("Hello from inside normal Function")
            return "Hello from inside normal Function"
        }
        const arrowFunction=()=>{
            console.log("Hello from inside arrow Function")
            return "Hello from inside arrow Function"
        }
        return{
            string:"Ali",
            integer:10,
            float:10.5,
            array:[1,2,3],
            "function":()=>{
                console.log("Hello Ali El-Mohammady")
                return "Ali El-Mohammady"
            },
            normalFunction:normalFunction(),
            arrowFunction:arrowFunction(),
            object:{"name":"ali"},
            html:markup("<button class='btn btn-primary' onClick='alert(Welcome to Dashboard)'>Show Alert</button>")
        }
    }

}


registry.category('services').add('basicServices', owlBasicServices);
