/** @odoo-module **/

import { registry } from '@web/core/registry';
const { Component, useState, onWillStart, useRef } = owl;
import { useService } from "@web/core/utils/hooks";

export class TodoListOwl extends Component {
    setup(){
        this.state = useState({
            task:{name:"", time:"", isCompleted:false},
            taskEdit:{name:"", time:""},
            taskList:[],
            isEdit: false,
            editingTaskId: null,
        })
        this.nameInput = useRef("name-input")
        this.timeInput = useRef("time-input")
        this.orm = useService("orm")
        this.model = "owl.todo.list.app"
        this.searchInput = useRef("search-input")

        onWillStart(async ()=>{
            await this.getAllTasks()
        })
    }

    async getAllTasks(){
        this.state.taskList = await this.orm.searchRead(this.model, [], [])
    }

    async addTask() {
        if (!this.state.task.name) {
            alert("Task Name is required, Please add it.");
            return;
        }
        if (this.state.task.time) {
            this.state.task.time = this.convertToOdooDatetime(this.state.task.time);
        } else {
            delete this.state.task.time
        }
        try {
            await this.orm.create(this.model, [this.state.task]);
            await this.getAllTasks();
            this.resetForm();
            this.state.isEdit=false;
        } catch (error) {
            alert("An error occurred while adding the task.");
        }
    }

    // Helper function to format the date for Odoo
    formatDateForOdoo(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-based
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');
        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    }

    convertToOdooDatetime(value) {
        if (!value) return null;
        if (value.includes("T")) {
            const [date, time] = value.split("T");
            return `${date} ${time}:00`;
        } else {
            return value;
        }
    }

    resetForm(){
        this.state.task = {name:"", time:"", isCompleted:false}
    }

    editTask(task){
        this.state.editingTaskId = task.id;
        this.state.taskEdit = {name:task.name, time:task.time};
    }

    async saveTask(record){
        if ( this.state.taskEdit.name != record.name ){
            const formattedTime = this.convertToOdooDatetime(this.state.taskEdit.time);
            await this.orm.write(this.model, [record.id], {name:this.state.taskEdit.name,time:formattedTime});

        }
        this.state.taskEdit = {name:"", time:""};
        this.state.editingTaskId = null;
        await this.getAllTasks();
    }



    async deleteTask(task){
        await this.orm.unlink(this.model, [task.id]);
        await this.getAllTasks();
    }

    async toggleTask(e, task){
        const updatedStatus = !task.isCompleted;
        await this.orm.write(this.model, [task.id], { isCompleted: updatedStatus });
        await this.getAllTasks()
    }

}

TodoListOwl.template = 'todo_app.TodoList'
registry.category('actions').add('todo_app.action_todo_list_owl_js', TodoListOwl);