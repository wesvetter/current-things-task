# About

An [xbar][gh-xbar] plugin that shows the current work task in Things 3.

![Screenshot of the plugin](preview.png)

The task must be scheduled for Today and be under an area called "Work" (either directly or in a project in the Work area).

## Requirements

*   [Xbar][gh-xbar]
*   Things 3 (obviously)
*   Python 3
*   The `things` Python package

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


[gh-xbar]: https://github.com/matryer/xbar
