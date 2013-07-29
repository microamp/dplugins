dplugins (dynamic plugins)
--------------------------
**dplugins** is a simple wxPython application with dynamic plugins. Individual
Python plugins found in subdirectories in the 'plugins' directory will be
dynamically loaded when the application first starts up. Each tab and button
correspond to a subdirectory and a Python plugin belonging to it respectively.

Each Python plugin must have the following attributes;
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
* The application outputs logging messages to a log file called 'output.log'.
