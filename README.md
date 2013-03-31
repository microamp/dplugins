__dplugins__ (dynamic plugins)

Individual Python plugins found in subdirectories in the 'plugins' directory
will be dynamically loaded when the application first starts up. Each tab and
button correspond to a subdirectory and a Python plugin under it respectively.

Each Python plugin MUST have the following attributes;
* `_id`: ID of the plugin (this is what the button will be labelled as)
* `_desc`: short description about the plugin
* `_func`: function to execute when an event is fired

The application outputs logging messages to a log file called 'output.log'.

Feel free to create a new subdirectory under 'plugins', and put your Python
plugins into the subdirectory.

This can be useful for storing implementation for doing simple administration
tasks, or just for testing stuff.
