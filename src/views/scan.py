#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx


class ChannelScan(wx.Frame):
    def __init__(self, parent=None):
        super(ChannelScan, self).__init__(
            parent=parent,
            title=u'Escaneo de canales'
        )

        panel = wx.Panel(parent=self)
        panel.SetBackgroundColour(wx.BLACK)

        self.btn_scan = wx.Button(parent=panel, label=u'Escanear')
        self.btn_continue = wx.Button(parent, label=u'Continuar')

        szr_buttons = wx.BoxSizer(wx.HORIZONTAL)
        szr_buttons.Add(self.btn_scan, flag=wx.RIGHT, border=2)
        szr_buttons.Add(self.btn_continue, flag=wx.RIGHT, border=2)

        self.SetSizer(szr_buttons)

