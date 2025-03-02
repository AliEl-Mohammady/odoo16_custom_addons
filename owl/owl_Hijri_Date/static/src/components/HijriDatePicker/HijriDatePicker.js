/** @odoo-module **/

import { _lt } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { loadCSS, loadJS } from "@web/core/assets";
const { DateTime } = luxon;


import { Component, useState, onMounted, onWillStart } from "@odoo/owl";
let HijriDatePickerId=0

export class HijriDatePickerField extends Component {
    setup() {
        console.log(">>>>>>>>>>>",this.props)
        this.HijriDatePickerId=`hijri_date_${HijriDatePickerId}`
        onWillStart(async() => {
            await loadJS("owl_Hijri_Date/static/src/lib/bootstrap-hijri-datetimepicker.min.js")
        })

        onMounted(()=>{
            $(`#${this.HijriDatePickerId}`).hijriDatePicker({
                hijri:true,
                format:'DD/MM/YYYY',
                hijriFormat:'iDD/iMM/iYYY'
            });
        })
    }

    onBlur(e){
        if(e.target.value){
          const date=DateTime.fromFormat(e.target.value,'dd/MM/YYYY');
          this.props.update(date);
        }else{
            this.props.update(false);
        }
    }

    get formattedValue(){
        return this.props.value?this.props.value.toFormat('dd/MM/YYYY'):""
    }
}


HijriDatePickerField.template = "owl_Hijri_Date.HijriDatePickerField";

HijriDatePickerField.props = {
    ...standardFieldProps,
};

HijriDatePickerField.displayName = _lt("Hijri Date Field");

HijriDatePickerField.supportedTypes = ["date"];

registry.category("fields").add("date_picker", HijriDatePickerField);
