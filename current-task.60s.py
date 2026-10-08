#!/usr/bin/python3
# Pin the system Python. SwiftBar runs plugins from a login shell, and
# `#!/usr/bin/env python3` follows PATH to Nix's python3.

#  <xbar.title>Current Things Task</xbar.title>
#  <xbar.version>v0.1</xbar.version>
#  <xbar.author>Wes Vetter</xbar.author>
#  <xbar.author.github>wesvetter</xbar.author.github>
#  <xbar.desc>Shows the current task in Things</xbar.desc>
#  <xbar.dependencies>python3</xbar.dependencies>

import json
import os
import subprocess

DEFAULT_AREA_NAME = 'Work'
DEFAULT_HIDDEN_LABEL = 'Hidden'
MAX_TITLE_LENGTH = 20
NO_TASKS_MESSAGE = '☑️'

# Record and unit separators keep titles that contain tabs or commas intact.
ROW_SEPARATOR = '\x1e'
FIELD_SEPARATOR = '\x1f'

# Read Today through Things' scripting interface. SwiftBar cannot open the
# Things SQLite database (macOS denies it), and `tell application` does not
# launch Things when it is quit.
TODAY_SCRIPT = r'''
if application "Things3" is not running then
  return "NOT_RUNNING"
end if

set us to ASCII character 31
set rs to ASCII character 30

tell application "Things3"
  set rows to ""
  repeat with td in to dos of list "Today"
    if status of td is open then
      set taskName to name of td
      set areaName to ""
      try
        set areaName to name of area of td
      end try
      if areaName is missing value or areaName is "" then
        try
          set areaName to name of area of project of td
        end try
      end if
      if areaName is missing value then set areaName to ""
      set tagText to ""
      try
        set tagText to tag names of td
      end try
      if tagText is missing value then set tagText to ""
      set row to taskName & us & areaName & us & tagText
      if rows is "" then
        set rows to row
      else
        set rows to rows & rs & row
      end if
    end if
  end repeat
  return rows
end tell
'''


def find_user_config():
    """
    Looks for a JSON configuration file in the user's home directory.
    """
    path_to_config_file = os.path.expanduser('~/.current-thing.json')

    if not os.path.exists(path_to_config_file):
        return {}

    with open(path_to_config_file, 'r') as file:
        return json.load(file)


def build_config():
    """
    Builds the configuration dictionary.
    """
    config = {
        'hidden_label': DEFAULT_HIDDEN_LABEL,
        'max_title_length': MAX_TITLE_LENGTH,
        'no_tasks_message': NO_TASKS_MESSAGE,
        'target_area_name': DEFAULT_AREA_NAME,
    }

    config.update(find_user_config())

    return config


def truncate_title(title, max_length):
    """
    Truncates the title to the specified length.
    """
    if len(title) > max_length:
        return title[:max_length] + '...'
    else:
        return title


def parse_today_output(output):
    """
    Parse the AppleScript payload into task dicts.

    `None` means Things is not running.
    """
    if output == 'NOT_RUNNING':
        return None

    if output == '':
        return []

    tasks = []
    for row in output.split(ROW_SEPARATOR):
        title, area, tags = (row.split(FIELD_SEPARATOR) + ['', ''])[:3]
        tasks.append({
            'title': title,
            'area': area,
            'tags': [tag.strip() for tag in tags.split(',') if tag.strip()],
        })
    return tasks


def select_current_task(tasks, config):
    """
    First Today task in the target area, skipping the hidden label.
    """
    area_name = config.get('target_area_name')
    if area_name is None:
        scoped = list(tasks)
    else:
        scoped = [task for task in tasks if task.get('area') == area_name]

    hidden_label = config.get('hidden_label')
    if hidden_label:
        scoped = [task for task in scoped if hidden_label not in task.get('tags', [])]

    if not scoped:
        return None
    return scoped[0]


def fetch_today_tasks():
    """
    Today's open to-dos, in Things' Today order.
    """
    completed = subprocess.run(
        ['/usr/bin/osascript', '-e', TODAY_SCRIPT],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if completed.returncode != 0:
        message = completed.stderr.strip() or 'osascript failed'
        raise RuntimeError(message)

    output = completed.stdout
    if output.endswith('\n'):
        output = output[:-1]
    return parse_today_output(output)


def find_current_task():
    """
    Finds the current task in Things, scoped by area.
    """
    config = build_config()

    try:
        tasks = fetch_today_tasks()
    except (OSError, subprocess.TimeoutExpired, RuntimeError):
        print('Things unavailable')
        return

    if tasks is None:
        print('Open Things')
        return

    current = select_current_task(tasks, config)
    if current:
        print(truncate_title(current['title'], config.get('max_title_length')))
    else:
        print(config.get('no_tasks_message'))


if __name__ == '__main__':
    find_current_task()
