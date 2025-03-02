/** @odoo-module */

import { registry } from "@web/core/registry"
import { formView } from "@web/views/form/form_view"
import { FormController } from "@web/views/form/form_controller"
import { useService } from "@web/core/utils/hooks"
const { useEffect }=owl;

class SaleOrderFormController extends FormController {
    setup(){
        super.setup()
//        console.log("This is Sale Order form controller",this)
        useEffect(() => {
            console.log("State is changed",this.model.root.data.state)
            this.disabledForm()
            },
            () => [this.model.root.data.state]
        );

        this.onNotebookPageChange = (notebookId, page) => {
            this.disabledForm()
        };
    }

    disabledForm(){
        const inputs=document.querySelectorAll(".o_form_sheet input");
        const fieldWidgets=document.querySelectorAll(".o_form_sheet .o_field_widget");
        const newState=this.model.root.data.state =='draft';

        if (newState){
           if (inputs) inputs.forEach(e=>e.setAttribute("disabled",1));
           if (fieldWidgets) fieldWidgets.forEach(e=>e.classList.add("pe-none"))
           this.canEdit=false
        }else{
            if (inputs) inputs.forEach(e=>e.removeAttribute("disabled"));
            if (fieldWidgets) fieldWidgets.forEach(e=>e.classList.remove("pe-none"))
            this.canEdit=true
        }
    }

    async beforeLeave() {
        console.log("inside beforeLeave")
        if (state=this.model.root.data.state =='draft') return
        super.beforeLeave()
    }

    async beforeUnload(ev) {
        console.log("inside beforeUnload")
        if (state=this.model.root.data.state =='draft') return
        super.beforeUnload()
    }
}

//SaleOrderFormController.template = "owl_disable_form.SaleOrderFormView"

export const SaleOrderFormView = {
    ...formView,
    Controller: SaleOrderFormController,
}

registry.category("views").add("sale_order_form_view", SaleOrderFormView)