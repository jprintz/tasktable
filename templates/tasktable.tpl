<html>
    <head>
        <title> TaskTable </title>
        <link rel="stylesheet" type="text/css" href="static/css/tasktable.css">
    </head>

    <body>
        <div>
            <h1>Welcome to the TaskTable</h1>
            <section class="task-form">
                <h2>Add a task</h2>
                <form action="/tasks/add" method="post" class="task-form-fields">
                    <label>
                        Project
                        <input type="text" name="project" required>
                    </label>
                    <label>
                        Title
                        <input type="text" name="title" required>
                    </label>
                    <label>
                        Status
                        <input type="text" name="status" required>
                    </label>
                    <label>
                        Priority
                        <select name="priority" required>
                            <option value="1">Critical</option>
                            <option value="2">High</option>
                            <option value="3">Normal</option>
                            <option value="4">Low</option>
                        </select>
                    </label>
                    <button type="submit">Add task</button>
                </form>
            </section>
% priorities = ["Critical", "High", "Normal", "Low"]
% priority_map = {"1": "Critical", "2": "High", "3": "Normal", "4": "Low"}
% projects = sorted({task["project"] for task in tasks})
            <div class="table-container" role="table">
                <div class="flex-table header" role="rowgroup">
                    <div class="flex-cell table-head">Project</div>
% for priority in priorities:
                    <div class="flex-cell table-head">{{priority}}</div>
% end
                </div>
% for project in projects:
                <div class="flex-row" role="rowgroup">
                    <div class="flex-cell projectCell" role="cell">{{project}}</div>
% for priority in priorities:
                    <div class="flex-cell" role="cell">
% for task in tasks:
% if task["project"] == project and priority_map.get(task["priority"]) == priority:
                        <div class="task-cell" role="cell"
                             data-task-id="{{task['id']}}"
                             data-task-project="{{task['project']}}"
                             data-task-title="{{task['title']}}"
                             data-task-status="{{task['status']}}"
                             data-task-priority="{{task['priority']}}">
                            <form action="/tasks/{{task['id']}}/delete" method="post" class="delete-form">
                                <button type="submit" class="delete-button" aria-label="Delete task">🗑</button>
                            </form>
                            <h3>{{task["title"]}}</h3>
                            <p>Status: {{task["status"]}}</p>
                            <button type="button" class="edit-button">Edit</button>
                        </div>
% end
% end
                    </div>
% end
                </div>
% end
            </div>
            <div class="modal" id="edit-modal" aria-hidden="true">
                <div class="modal-content" role="dialog" aria-modal="true" aria-labelledby="edit-modal-title">
                    <div class="modal-header">
                        <h2 id="edit-modal-title">Edit task</h2>
                        <button type="button" class="modal-close" aria-label="Close">×</button>
                    </div>
                    <form id="edit-form" method="post" class="task-form-fields">
                        <label>
                            Project
                            <input type="text" name="project" id="edit-project" required>
                        </label>
                        <label>
                            Title
                            <input type="text" name="title" id="edit-title" required>
                        </label>
                        <label>
                            Status
                            <input type="text" name="status" id="edit-status" required>
                        </label>
                        <label>
                            Priority
                            <select name="priority" id="edit-priority" required>
                                <option value="1">Critical</option>
                                <option value="2">High</option>
                                <option value="3">Normal</option>
                                <option value="4">Low</option>
                            </select>
                        </label>
                        <div class="modal-actions">
                            <button type="button" class="modal-cancel">Cancel</button>
                            <button type="submit">Save</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        <script>
            const modal = document.getElementById('edit-modal');
            const editForm = document.getElementById('edit-form');
            const editProject = document.getElementById('edit-project');
            const editTitle = document.getElementById('edit-title');
            const editStatus = document.getElementById('edit-status');
            const editPriority = document.getElementById('edit-priority');

            function openModal(taskCell) {
                const taskId = taskCell.dataset.taskId;
                editForm.action = `/tasks/${taskId}/update`;
                editProject.value = taskCell.dataset.taskProject || '';
                editTitle.value = taskCell.dataset.taskTitle || '';
                editStatus.value = taskCell.dataset.taskStatus || '';
                editPriority.value = taskCell.dataset.taskPriority || '3';
                modal.classList.add('is-open');
                modal.setAttribute('aria-hidden', 'false');
            }

            function closeModal() {
                modal.classList.remove('is-open');
                modal.setAttribute('aria-hidden', 'true');
            }

            document.querySelectorAll('.edit-button').forEach((button) => {
                button.addEventListener('click', (event) => {
                    const taskCell = event.currentTarget.closest('.task-cell');
                    if (taskCell) {
                        openModal(taskCell);
                    }
                });
            });

            modal.addEventListener('click', (event) => {
                if (event.target === modal) {
                    closeModal();
                }
            });

            document.querySelectorAll('.modal-close, .modal-cancel').forEach((button) => {
                button.addEventListener('click', closeModal);
            });
        </script>
    </body>
</html>
