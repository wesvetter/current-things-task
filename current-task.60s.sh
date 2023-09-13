#!/bin/bash

#  <xbar.title>Current Things Task</xbar.title>
#  <xbar.version>v0.1</xbar.version>
#  <xbar.author>Wes Vetter</xbar.author>
#  <xbar.author.github>wesvetter</xbar.author.github>
#  <xbar.desc>Shows the current task in Things</xbar.desc>
#  <xbar.dependencies>python3</xbar.dependencies>

# Use this if you get an application error trying to use the Python script on
# legacy versions of macOS. These may attempt to use an Xcode library function
# that does not exist on your system.

# Change these to your needs:
PYTHON_PATH=/usr/local/opt/python/libexec/bin/python
SCRIPT_PATH=~/Desktop/Code/current-things-task/current-task.60s.py

# Run the script and output to stdout.
output=$($PYTHON_PATH $SCRIPT_PATH)
echo $output
