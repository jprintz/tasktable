<html>
    <head>
        <title> TaskTable </title>
        <link rel="stylesheet" type="text/css" href="static/css/tasktable.css">
    </head>

    <body>
        <div>
            <h1>Welcome to the TaskTable</h1>
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
                        <div class="task-cell" role="cell">
                            <h3>{{task["title"]}}</h3>
                            <p>Status: {{task["status"]}}</p>
                        </div>
% end
% end
                    </div>
% end
                </div>
% end
            </div>
        </div>
    </body>
</html>
