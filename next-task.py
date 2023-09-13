#!/usr/bin/env python3

try:
    import things
except ImportError:
    print("Error: The 'things' package is not installed. Please install it using the following command:")
    print("pip install things")
    exit()

todays_tasks = things.today()

# Find the Work area.
work_area = [a for a in things.areas() if a.get('title') == 'Work'][0]

# Get all tasks in the Work area.
work_tasks = things.tasks(area=work_area.get('uuid'))

# Get all projects in the Work area.
work_projects = things.projects(area=work_area.get('uuid'))

# Get all todos of projects in the Work area.
work_project_todos = [t for p in work_projects for t in things.todos(project=p.get('uuid'))]

# Add the project todos to the work tasks.
work_tasks.extend(work_project_todos)

# Find the intersection of today's tasks and the work tasks.
todays_work_tasks = [t for t in todays_tasks if t in work_tasks]

# get the first task in the list.
next_task = todays_work_tasks[0]

# print the title of the task.
print(next_task['title'] or 'nada')
