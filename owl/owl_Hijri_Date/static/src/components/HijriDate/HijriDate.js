/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { DateField } from "@web/views/fields/date/date_field";
import { DateTimeField } from "@web/views/fields/datetime/datetime_field";
import { registry } from "@web/core/registry";
const { Component, onWillStart, useRef,useState} = owl
const { DateTime } = luxon;

patch(DateField.prototype, "date_calender", {
    setup() {
        this._super()
        this.calender = useState({
            "hebrew":this.setCalender(this.props.value,"hebrew"),
            "islamic":this.setCalender(this.props.value,"islamic")
        })
        console.log(this.props.value)
    },
    onDateTimeChanged(date) {
        this._super(date);
        this.calender.islamic=this.setCalender(date,"islamic")
    },
    get formattedValue() {
        return this.isDateTime
            ? this.setCalender(this.props.value,"islamic",DateTime.DATE_MED)
            : this.setCalender(this,props.value,"islamic");
    },
    setCalender(date,calender,format=DateTime.DATE_FULL){
        return date && date.reconfigure({ outputCalendar:calender}).toLocaleString(format)
    },

});


patch(DateTimeField.prototype, "datetime_calender", {
    setup() {
        this._super()
        this.calender = useState({
            "hebrew":this.setCalender(this.props.value,"hebrew"),
            "islamic":this.setCalender(this.props.value,"islamic")
        })
        console.log(this.props.value)
    },
    onDateTimeChanged(date) {
        this._super(date);
        this.calender.islamic=this.setCalender(date,"islamic")
    },
    get formattedValue() {
        return  this.setCalender(this,props.value,"islamic");
    },
    setCalender(date,calender){
        return date && date.reconfigure({ outputCalendar:calender}).toLocaleString(DateTime.DATETIME_MED)
    },

});
