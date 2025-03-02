/** @odoo-module **/

import { registry } from '@web/core/registry';
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { getDefaultConfig } from "@web/views/view";
import { loadCSS, loadJS } from "@web/core/assets";

const { Component, useState, onWillStart, onMounted, useRef,useSubEnv } = owl;

export class OwlDashboardExternalLib extends Component {
    setup(){
        this.phone = useRef("phone");
        this.file = useRef("file");
        this.state=useState({
            validNumber:undefined
        })
        this.display={
            controlPanel:{"top-right":false,"bottom-right":false}
        }
        useSubEnv({
            config: {
                ...getDefaultConfig(),
                ...this.env.config,
            }
        });
        console.log("Dashboard Ex Lib");
        onWillStart(async ()=>{
//            await loadCSS('https://cdn.jsdelivr.net/npm/intl-tel-input@25.2.1/build/css/intlTelInput.css');  //or use lib file to add ext libraries
//            await loadJS('https://cdn.jsdelivr.net/npm/intl-tel-input@25.2.1/build/js/intlTelInput.min.js');
            await loadCSS('/owl_external_libraries/static/src/lib/intel-tel-input/build/css/intlTelInput.css');  //or use lib file to add ext libraries
            await loadJS('/owl_external_libraries/static/src/lib/intel-tel-input/build/js/intlTelInput.min.js');

            await loadCSS('https://unpkg.com/filepond@^4/dist/filepond.css');
            await loadJS('https://unpkg.com/filepond@^4/dist/filepond.js');
            await loadCSS('https://unpkg.com/filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css');
            await loadJS('https://unpkg.com/filepond-plugin-image-preview/dist/filepond-plugin-image-preview.js');
        })

        onMounted(()=>{
            console.log("Hello",intlTelInput);
            this.phoneFormat=intlTelInput(this.phone.el,{
                utilsScript:"/owl_external_libraries/static/src/lib/intel-tel-input/build/js/utils.js"
            })
            FilePond.registerPlugin(FilePondPluginImagePreview);
            this.filePond=FilePond.create(this.file.el,{
                allowMultiple:true,
                server: {
                    process: './file/process',
                    fetch: null,
                    revert: './file/revert',
                },
            })
            console.log("FilePond",FilePond)
            console.log("this.filePond",this.filePond)

        })
    }

    validate(){
        if (this.phoneFormat.isvalidNumber){
            this.state.validNumber=true
        }else{
            this.state.validNumber=false
        }
    }

}

OwlDashboardExternalLib.template = 'owl_external_libraries.OwlDashboardExternalLibView'
OwlDashboardExternalLib.components = {Layout}

registry.category('actions').add('owl_external_libraries.action_odoo_dashboard_external_library_owl_js', OwlDashboardExternalLib);