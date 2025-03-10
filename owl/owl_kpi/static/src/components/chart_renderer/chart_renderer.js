/** @odoo-module **/

import { registry } from "@web/core/registry";
import { loadJS } from "@web/core/assets";
const { Component, onWillStart, useRef,onMounted} = owl

export class ChartRenderer extends Component {
            setup(){
                this.chartRef = useRef("chart")
                onWillStart (async()=>{
                await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js")})

                onMounted(()=>this.renderChart())

            };

            renderChart(){
                new Chart(this.chartRef.el,
                 {
                      type: this.props.type,
                      data: this.props.config,
                      options :{
                        responsive :true,
                        plugins :{
                          legend :{
                              position :'bottom',
                          },
                          title:{
                          display:true,
                          position:'bottom',
                          text:this.props.title}
                        }
                      }
                 });
            }
}

ChartRenderer.template="owl.ChartRenderer"

