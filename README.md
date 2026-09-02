# About

A [SwiftBar][gh-swiftbar] plugin that shows the current work task in Things 3.

![Screenshot of the plugin](preview.png)

The task must be scheduled for Today and can be filtered to a specific area (by default "Work", but this is configurable).

## Requirements

*   [SwiftBar][gh-swiftbar]
*   [Things 3][things-www] (obviously)
*   Python 3
*   The `things.py` Python package

## Installation

1.  Install SwiftBar (if you don't already have it):

    ```
    brew install --cask swiftbar
    ```

    On first launch, set the Plugin Folder to
    `~/Library/Application Support/SwiftBar/Plugins` (or any folder you prefer).

2.  Clone the repo:

    ```
    git clone git@github.com:wesvetter/current-things-task.git
    ```

3.  Install the `things` Python package:

    ```
    /usr/bin/pip3 install things.py
    ```

    (View the `.py` file for instructions on using Python via Homebrew)

4.  Link the script to your SwiftBar plugin directory.

    ```
    cd current-things-task
    mkdir -p "$HOME/Library/Application Support/SwiftBar/Plugins"
    ln -s "$PWD/current-task.60s.py" "$HOME/Library/Application Support/SwiftBar/Plugins/current-task.60s.py"
    ```

## Configuration

The plugin can be customized by creating a `.current-thing.json` file in your home directory.

Example:

```json
{
  "target_area_name": "Family",
  "no_tasks_message": "all done!"
}
```

### `target_area_name`

**default:** `Work`

The specified Area in Things to filter by. This is useful because you may not want your _actual_ current task (say, "Call the electrician") visible.

Tasks from projects under this area will also appear.

To not filter by any area, set this value to `null`. The plugin will then show whatever task is next for the day.

### `no_tasks_message`

**default:**  ☑️

A message to display when no remaining tasks in the target area are left for today.

### `max_title_length`

**default:** 20

The maximum length of the title before truncation. If the title is longer than this, it will be truncated and `...` will be appended. 

Note that if the title is excessively long, such that it collides with other application's menus, then SwiftBar will not render the plugin at all.

### `hidden_label`

**default:** `Hidden`

This is a label that, if added to a task, will exclude it from appearing in status bar. This can be useful if the task is sensitive (e.g. "Fire Johnny" or "Search for new job").

[gh-swiftbar]: https://github.com/swiftbar/SwiftBar
[things-www]: https://culturedcode.com/things/
