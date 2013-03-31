#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import os.path
import sys
import time
import glob
import imp
import logging
from datetime import datetime

import wx


PLUGINS_DIR = "plugins"

# configure logger
logging.basicConfig(
    filename="output.log",
    format="%(asctime)s - %(name)s - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)


class DynamicPluginsFrame(wx.Frame):
    def __init__(self, title, size=(400, 500)):
        """Initialise the main frame."""
        wx.Frame.__init__(
            self,
            None,
            wx.ID_ANY,
            title,
            size=size,
            style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE,
        )
        self.build()

    def build(self):
        """Build the UI."""
        self.CreateStatusBar()  # status bar
        main_sizer = wx.BoxSizer(wx.VERTICAL)  # sizer

        # path to plugins directory
        path = os.path.join(os.getcwd(), PLUGINS_DIR)
        plugin_dirs = [d for d in sorted(os.listdir(path))
                       if os.path.isdir(os.path.join(path, d))]
        logging.debug("plugin directories found: %s" % ", ".join(plugin_dirs))

        self.funcmapper = {}

        # plugins directories and their plugins loaded and added to main frame
        self.nb = wx.Notebook(self, -1, style=wx.NB_TOP)
        for plugin_dir in plugin_dirs:
            panel = wx.Panel(self.nb)
            self.add_plugins(
                self.load_plugins(glob.glob(
                    os.path.join(os.path.join(path, plugin_dir), "*.py"))
                ),
                panel,
                plugin_dir,
            )

        # message output list control
        self.msgoutput = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.msgoutput.InsertColumn(0, "message output",
                                    width=self.GetSize()[1])
        self.msgoutput.SetBackgroundColour(wx.NamedColour("LIGHT GREY"))

        # items added to sizer
        main_sizer.Add(self.nb, 0, wx.EXPAND)
        main_sizer.Add(self.msgoutput, 1, wx.EXPAND)

        # set up sizer
        self.SetSizer(main_sizer)
        self.Show(True)

    def on_menuitem(self, evt):
        """Show a message dialog when a menu item even is fired."""
        dlg = wx.MessageDialog(
            self,
            "message 1",
            "message 2",
            wx.OK | wx.ICON_INFORMATION
        )
        dlg.ShowModal()
        dlg.Destroy()

    def load_plugins(self, plugins):
        """Set up attributes in each plugin."""
        loaded = []
        for plugin in plugins:
            name = os.path.splitext(os.path.basename(plugin))[0]

            temp = {}
            temp[name] = imp.load_source(name, plugin)
            temp[name].os = os
            temp[name].sys = sys
            temp[name].time = time
            temp[name].wx = wx
            temp[name].datetime = datetime
            temp[name].logging = logging

            loaded.append((
                temp[name]._name,
                temp[name]._desc,
                temp[name]._func,
            ))
        return loaded

    def add_plugins(self, plugins, panel, plugin_dir):
        """Add each plugin to a panel it belongs to."""
        sizer = wx.FlexGridSizer(rows=len(plugins), cols=2)
        sizer.AddGrowableCol(1)
        for plugin in sorted(plugins):
            name, desc, func = plugin[0], plugin[1], plugin[2]
            # button (name)
            button = wx.Button(panel, wx.NewId(), name)
            sizer.Add(button, -1, wx.EXPAND)
            # label (desc)
            label = wx.StaticText(panel, -1, desc)
            sizer.Add(label, -1, wx.ALIGN_CENTRE_VERTICAL)
            # event handler (func)
            self.funcmapper[button.GetId()] = func
            self.Bind(wx.EVT_BUTTON, self.issue, button)

        panel.SetSizer(sizer)
        self.nb.AddPage(panel, plugin_dir)  # directory name = tab title
        logging.debug("page added: '{}'".format(plugin_dir))

    def issue(self, event):
        """Call a plugin function based on the event fired."""
        try:
            self.funcmapper[event.GetId()](self)
        except Exception as e:
            logging.error(e)
            dlg = wx.MessageDialog(
                self,
                str(e),
                "error",
                style=wx.ICON_ERROR | wx.OK
            )
            dlg.ShowModal()
            dlg.Destroy()

    def output(self, text):
        """Display the message in the 'output' area."""
        index = self.msgoutput.InsertStringItem(sys.maxint, "")
        self.msgoutput.SetStringItem(
            index,
            0,
            "[{ts}] {msg}".format(
                ts=datetime.strftime(datetime.now(), "%H:%M:%S"),
                msg=text,
            )
        )
        self.msgoutput.EnsureVisible(self.msgoutput.GetItemCount()-1)
        logging.debug(text)

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = DynamicPluginsFrame("dynamic plugins", size=(500, 600))
    app.MainLoop()
