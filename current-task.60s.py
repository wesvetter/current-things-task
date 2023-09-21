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

import os
import sys
import json

DEFAULT_AREA_NAME = 'Work'
MAX_TITLE_LENGTH = 20
NO_TASKS_MESSAGE = '☑️'

try:
    import things
except ImportError:
    # Error: The 'things' package is not installed. Please install it using the following command:
    print("pip install things.py")
    exit()


def find_user_config():
    """
    Looks for a JSON configuration file.

    By default looks in the current directory, then in the user's home directory.
    """
    repo_directory = os.path.dirname(os.path.abspath(__file__))
    default_path = os.path.join(repo_directory, '.current-thing.json')
    path_to_read = None

    if os.path.exists(default_path):
        path_to_read = default_path

    if os.path.exists(os.path.expanduser('~/.current-thing.json')):
        path_to_read = os.path.expanduser('~/.current-thing.json')

    if not path_to_read:
        return {}

    with open(path_to_read, 'r') as file:
        return json.load(file)


def build_config():
    """
    Builds the configuration dictionary.
    """
    config = {
        'max_title_length': MAX_TITLE_LENGTH,
        'no_tasks_message': NO_TASKS_MESSAGE,
        'target_area_name': DEFAULT_AREA_NAME
    }

    config.update(find_user_config())

    return config


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

    # Add the project todos to the area tasks.
    area_tasks.extend(area_project_todos)

    return area_tasks


def truncate_title(title, max_length):
    """
    Truncates the title to the specified length.
    """
    if len(title) > max_length:
        return title[:max_length] + '...'
    else:
        return title


def find_current_task():
    """
    Finds the current task in Things, scoped by area.
    """
    todays_tasks = things.today()

    config = build_config()

    scoped_tasks = find_all_todos_by_area_title(config.get('target_area_name'))

    # Find the intersection of today's tasks and the area's tasks.
    todays_scoped_tasks = [t for t in todays_tasks if t in scoped_tasks]

    if todays_scoped_tasks:
        next_task = todays_scoped_tasks[0]
        title = truncate_title(next_task['title'], config.get('max_title_length'))
        print(title)
    else:
        print(config.get('no_tasks_message'))

find_current_task()
