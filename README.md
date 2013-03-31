dplugins (Dynamic Plugins)
==========================
**dplugins** is a simple wxPython application with dynamic plugins. Individual
Python plugins found in subdirectories in the 'plugins' directory will be
dynamically loaded when the application first starts up. Each tab and button
correspond to a subdirectory and a Python plugin belonging to it respectively.

Each Python plugin MUST have the following attributes;
* `_name`: name of the plugin (this is what corresponding buttons will be
           labelled as)
* `_desc`: short description about the plugin
* `_func`: function to execute when an event is fired

Requirements
------------
* Python: 2.7.3
* wxPython: 2.8

Usage
-----
`python dplugins.py`

Further Notes
-------------
* This application was first developed to demonstrate my coding style.
* The application can be useful for storing implementation for doing simple
administration tasks, or just for testing stuff. Feel free to create a new
subdirectory under 'plugins', and put your Python plugins into the
subdirectory.
* The application outputs logging messages to a log file called 'output.log'.
