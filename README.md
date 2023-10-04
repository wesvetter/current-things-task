# About

An [xbar][gh-xbar] plugin that shows the current work task in Things 3.

![Screenshot of the plugin](preview.png)

The task must be scheduled for Today and can be filtered to a specific area (by default "Work", but this is configurable).

## Requirements

*   [Xbar][gh-xbar]
*   [Things 3][things-www] (obviously)
*   Python 3
*   The `things.py` Python package

## Installation

1.  Clone the repo:

    ```
    git clone git@github.com:wesvetter/current-things-task.git
    ```

2.  Install the `things` Python package:

    ```
    /usr/bin/pip3 install things.py
    ```

    (View the `.py` file for instructions on using Python via Homebrew)

3.  Link the script to your Xbar plugin directory.

    ```
    cd current-things-task
    ln -s $PWD/current-task.60s.py $HOME/Library/Application\ Support/xbar/plugins/current-task.60s.py
    ```

## Configuration

The Xbar plugin can be customized by creating a `.current-thing.json` file in your home directory.

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

Note that if the title is excessively long, such that it collides with other application's menus, then Xbar will not render plugin at all.


[gh-xbar]: https://github.com/matryer/xbar
[things-www]: https://culturedcode.com/things/
