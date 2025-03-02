/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";

patch(ListController.prototype, "school_student_list_view", {
    setup() {
        this._super.apply();
        this.action = useService("action");
    },
    editSchoolStudent() {
        const activeIds = this.props.context.active_ids || [];
         console.log(">>>>>>>>>>>>>>",activeIds)// Access the active_ids from the current context
         console.log(">>>>>>>>>>>>>>",this.model.root.selection.map((record) => record.resId))// Access the active_ids from the current context
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Update fees",
            res_model: "student.fees.update.wizard",
            view_mode: "form",
            target: "new",
            views: [[false, "form"]],
            context: '{"default_students_ids": ['+this.model.root.selection.map((record) => record.resId)+'] }',
        });
    },

});
