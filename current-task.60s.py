#!/usr/bin/env python3
# By default use the system Python 3 installation.

# If Homebrew is installed, you can use the Homebrew Python 3 installation by
# replacing the default shebang line above with the following line (check
# `which python` and adjust the path as needed).
#!/usr/bin/env /opt/homebrew/opt/python@3.11/libexec/bin/python

#  <xbar.title>Current Things Task</xbar.title>
#  <xbar.version>v0.1</xbar.version>
#  <xbar.author>Wes Vetter</xbar.author>
#  <xbar.author.github>wesvetter</xbar.author.github>
#  <xbar.desc>Shows the current task in Things</xbar.desc>
#  <xbar.dependencies>python3</xbar.dependencies>

# The Python script may not work on legacy macOS versions (Big Sur or earlier),
# because it may not find the correct path to the Python executable. If that
# happens, use the shell script instead and specify the appropriate path to the
# Python executable (use `which python3` to find the path).
MAX_TITLE_LENGTH = 20

DEFAULT_AREA_NAME = 'Work'

try:
    import things
except ImportError:
    # Error: The 'things' package is not installed. Please install it using the following command:
    print("pip install things")
    exit()

def find_all_todos_by_area_title(title):
    """
    Finds all of the todos in the specified area, including those in projects.
    """
    try:
        target_area = [a for a in things.areas() if a.get('title') == title][0]
    except IndexError:
       raise Exception('Area not found: ' + title)

    # Get all tasks in the target area.
    area_tasks = things.tasks(area=target_area.get('uuid'))

    # Get all projects in the target area.
    area_projects = things.projects(area=target_area.get('uuid'))

    # Get all todos of projects in the target area.
    area_project_todos = [t for p in area_projects for t in things.todos(project=p.get('uuid'))]

    # Add the project todos to the work tasks.
    area_tasks.extend(area_project_todos)

    return things.tasks(area=target_area.get('uuid'))

todays_tasks = things.today()

work_tasks = find_all_todos_by_area_title(DEFAULT_AREA_NAME)

# Find the intersection of today's tasks and the work tasks.
todays_work_tasks = [t for t in todays_tasks if t in work_tasks]

if todays_work_tasks:
    # Get the first task in the list.
    next_task = todays_work_tasks[0]

    # Get the title of the task, and if it is longer than N characters truncate it.
    title = ''
    if len(next_task['title']) > MAX_TITLE_LENGTH:
        title = next_task['title'][:MAX_TITLE_LENGTH] + '...'
    else:
        title = next_task['title']

    # Print the title of the task.
    print(title)
else:
    print('☑️')
