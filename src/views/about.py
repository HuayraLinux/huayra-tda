#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.html

class AboutDialog(wx.Frame):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(
            parent=parent,
            title=u'Acerca de',
            style=wx.DEFAULT_FRAME_STYLE & ~wx.CLOSE_BOX
        )

        self._pref= wx.GetApp().preferences

        titular = wx.Panel(parent=self)
        txt = wx.StaticText(parent=titular, label="Acerca de Huayra TDA")
        txt.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        szr_titular = wx.BoxSizer(wx.HORIZONTAL)
        szr_titular.Add(txt)
        titular.SetSizer(szr_titular)

        panel = wx.Panel(parent=self)

        self.btn_close = wx.Button(parent=panel, label=u'Cerrar')
        self.btn_close.Bind(wx.EVT_BUTTON, self.OnClose)

        szr_buttons = wx.BoxSizer(wx.HORIZONTAL)
        szr_buttons.Add(self.btn_close, flag=wx.RIGHT, border=2)

        self.szr_panel = wx.BoxSizer(wx.VERTICAL)
        self.szr_panel.Add(szr_buttons)
        panel.SetSizer(self.szr_panel)

        # --
        self.messages = wx.html.HtmlWindow(parent=self)
        self.messages.SetPage(self._pref.load_html('about'))

        # --

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(titular, flag=wx.LEFT|wx.ALL, border=5)
        sizer.Add(self.messages, 1, flag=wx.EXPAND)
        sizer.Add(panel, flag=wx.ALL|wx.CENTER, border=5)

        self.SetSizer(sizer)

        self.SetMinSize((650, 450))
        self.Center()

    def OnClose(self, evt):
        self.Close()





