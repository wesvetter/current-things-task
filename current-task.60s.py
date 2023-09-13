#!/usr/bin/env python3

#  <xbar.title>Current Things Task</xbar.title>
#  <xbar.version>v0.1</xbar.version>
#  <xbar.author>Wes Vetter</xbar.author>
#  <xbar.author.github>wesvetter</xbar.author.github>
#  <xbar.desc>Shows the current task in Things</xbar.desc>
#  <xbar.image>http://www.hosted-somewhere/pluginimage</xbar.image>
#  <xbar.dependencies>python3</xbar.dependencies>
#  <xbar.abouturl>http://example.com/</xbar.abouturl>


# LEAVING OFF: The Python script seems to work but it isn't outputting anything
# in xbar. I put the plugin in ~/Library/Application Support/plugins and made
# it executable.


try:
    import things
except ImportError:
    # Error: The 'things' package is not installed. Please install it using the following command:
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
