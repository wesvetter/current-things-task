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
