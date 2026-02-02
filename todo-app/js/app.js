// Modern Todo List Application
class TodoApp {
    constructor() {
        this.tasks = JSON.parse(localStorage.getItem('tasks')) || [];
        this.currentFilter = 'all';
        this.init();
    }

    init() {
        this.renderTasks();
        this.updateTaskCount();
        this.bindEvents();
        this.showEmptyState();
    }

    bindEvents() {
        const taskInput = document.getElementById('taskInput');
        const addTaskBtn = document.getElementById('addTaskBtn');
        const clearCompletedBtn = document.getElementById('clearCompletedBtn');
        const filterBtns = document.querySelectorAll('.filter-btn');

        // Add task events
        addTaskBtn.addEventListener('click', () => this.addTask());
        taskInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.addTask();
            }
        });

        // Clear completed tasks
        clearCompletedBtn.addEventListener('click', () => this.clearCompleted());

        // Filter events
        filterBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setFilter(e.target.dataset.filter);
            });
        });
    }

    addTask() {
        const taskInput = document.getElementById('taskInput');
        const text = taskInput.value.trim();

        if (text) {
            const newTask = {
                id: Date.now(),
                text: text,
                completed: false,
                createdAt: new Date().toISOString()
            };

            this.tasks.unshift(newTask);
            this.saveTasks();
            this.renderTasks();
            this.updateTaskCount();
            this.showEmptyState();

            taskInput.value = '';
            taskInput.focus();
        }
    }

    deleteTask(id) {
        const taskElement = document.querySelector(`[data-id="${id}"]`);
        if (taskElement) {
            taskElement.classList.add('removing');
            
            setTimeout(() => {
                this.tasks = this.tasks.filter(task => task.id !== id);
                this.saveTasks();
                this.renderTasks();
                this.updateTaskCount();
                this.showEmptyState();
            }, 300);
        }
    }

    toggleTask(id) {
        this.tasks = this.tasks.map(task => {
            if (task.id === id) {
                return { ...task, completed: !task.completed };
            }
            return task;
        });
        
        this.saveTasks();
        this.renderTasks();
        this.updateTaskCount();
    }

    editTask(id, newText) {
        if (newText.trim()) {
            this.tasks = this.tasks.map(task => {
                if (task.id === id) {
                    return { ...task, text: newText.trim() };
                }
                return task;
            });
            
            this.saveTasks();
            this.renderTasks();
        }
    }

    clearCompleted() {
        this.tasks = this.tasks.filter(task => !task.completed);
        this.saveTasks();
        this.renderTasks();
        this.updateTaskCount();
        this.showEmptyState();
    }

    setFilter(filter) {
        this.currentFilter = filter;
        
        // Update active filter button
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        event.target.classList.add('active');
        
        this.renderTasks();
    }

    getFilteredTasks() {
        switch (this.currentFilter) {
            case 'active':
                return this.tasks.filter(task => !task.completed);
            case 'completed':
                return this.tasks.filter(task => task.completed);
            default:
                return this.tasks;
        }
    }

    renderTasks() {
        const taskList = document.getElementById('taskList');
        const filteredTasks = this.getFilteredTasks();
        
        taskList.innerHTML = '';

        filteredTasks.forEach(task => {
            const li = document.createElement('li');
            li.className = 'task-item';
            li.dataset.id = task.id;

            li.innerHTML = `
                <div class="task-checkbox ${task.completed ? 'checked' : ''}" 
                     onclick="todoApp.toggleTask(${task.id})">
                </div>
                <div class="task-text ${task.completed ? 'completed' : ''}">
                    ${this.escapeHtml(task.text)}
                </div>
                <div class="task-actions">
                    <button class="edit-btn" onclick="todoApp.showEditModal(${task.id}, '${this.escapeHtml(task.text)}')">✎</button>
                    <button class="delete-btn" onclick="todoApp.deleteTask(${task.id})">×</button>
                </div>
            `;

            taskList.appendChild(li);
        });
    }

    showEditModal(id, currentText) {
        const newText = prompt('編輯任務:', currentText);
        if (newText !== null) {
            this.editTask(id, newText);
        }
    }

    updateTaskCount() {
        const activeTasks = this.tasks.filter(task => !task.completed).length;
        const totalTasks = this.tasks.length;
        
        document.getElementById('taskCount').textContent = 
            `${activeTasks} 個待完成 / ${totalTasks} 個總計`;
    }

    showEmptyState() {
        const emptyState = document.getElementById('emptyState');
        const taskList = document.getElementById('taskList');
        
        if (this.getFilteredTasks().length === 0) {
            emptyState.classList.add('visible');
        } else {
            emptyState.classList.remove('visible');
        }
    }

    saveTasks() {
        localStorage.setItem('tasks', JSON.stringify(this.tasks));
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the app when the page loads
let todoApp;

document.addEventListener('DOMContentLoaded', () => {
    todoApp = new TodoApp();
});

// Export for global access
window.TodoApp = TodoApp;