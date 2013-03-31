def plugins_1_1(self):
    dlg = wx.MessageDialog(
        self,
        "are you sure?\n(it's okay to yes)",
        "test dialog",
        style=wx.ICON_QUESTION | wx.YES_NO,
    )
    msg = "successful" if dlg.ShowModal() == wx.ID_YES else "cancelled"
    self.output(msg)
    dlg.Destroy()

_name = "plugin 1-1"
_desc = "plugins/plugins_1/plugin_1-1.py"
_func = plugins_1_1
