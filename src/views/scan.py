#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.html
import wx.lib.scrolledpanel as scrolled


class ChannelScan(wx.Frame):
    def __init__(self, parent=None):
        super(ChannelScan, self).__init__(
            parent=parent,
            title=u'Escaneo de canales'
        )

        self._pref= wx.GetApp().preferences

        titular = wx.Panel(parent=self)
        txt = wx.StaticText(parent=titular, label="Búsqueda de canales")
        txt.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        szr_titular = wx.BoxSizer(wx.HORIZONTAL)
        szr_titular.Add(txt)
        titular.SetSizer(szr_titular)

        panel = wx.Panel(parent=self)

        self.btn_scan = wx.Button(parent=panel, label=u'Escanear')
        self.btn_scan_cancel = wx.Button(parent=panel, label=u'Cancelar')
        self.btn_close = wx.Button(parent=panel, label=u'Cerrar')
        self.btn_close.Bind(wx.EVT_BUTTON, self.OnClose)

        szr_buttons = wx.BoxSizer(wx.HORIZONTAL)
        szr_buttons.Add(self.btn_scan, flag=wx.RIGHT, border=2)
        szr_buttons.Add(self.btn_scan_cancel, flag=wx.RIGHT, border=2)
        szr_buttons.Add(self.btn_close, flag=wx.RIGHT, border=2)
        panel.SetSizer(szr_buttons)

        # --
        self.messages = wx.html.HtmlWindow(parent=self)
        self.messages.SetPage(self._pref.load_html('scan_start'))

        # --

        #self.progress_txt = wx.StaticText(parent=self, label="Escanendo %s")
        #self.gauge = wx.StaticText(parent=self, label="Escanendo %s")
        # --

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(titular, flag=wx.LEFT|wx.ALL, border=5)
        sizer.Add(self.messages, 1, flag=wx.EXPAND)
        sizer.Add(panel, flag=wx.ALL|wx.CENTER, border=5)

        self.SetSizer(sizer)

        self.SetMinSize((450, 300))
        self.Center()

    def OnClose(self, evt):
        self.Close()

