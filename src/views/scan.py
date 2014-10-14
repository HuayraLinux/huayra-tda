#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.html
from wx.lib.pubsub import Publisher


class ChannelScan(wx.Frame):
    def __init__(self, scanner, parent=None):
        super(ChannelScan, self).__init__(
            parent=parent,
            title=u'Escaneo de canales',
            style=wx.DEFAULT_FRAME_STYLE & ~wx.CLOSE_BOX
        )

        self._scanner = scanner
        self._pref= wx.GetApp().preferences

        titular = wx.Panel(parent=self)
        txt = wx.StaticText(parent=titular, label="Búsqueda de canales")
        txt.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        szr_titular = wx.BoxSizer(wx.HORIZONTAL)
        szr_titular.Add(txt)
        titular.SetSizer(szr_titular)

        panel = wx.Panel(parent=self)

        self.btn_scan = wx.Button(parent=panel, label=u'Escanear')
        self.btn_scan.Bind(wx.EVT_BUTTON, self.OnScan)
        self.btn_scan_cancel = wx.Button(parent=panel, label=u'Cancelar')
        self.btn_close = wx.Button(parent=panel, label=u'Cerrar')
        self.btn_close.Bind(wx.EVT_BUTTON, self.OnClose)

    # -
        self.progress_txt = wx.StaticText(parent=panel, label="-", style=wx.ALIGN_CENTRE)
        self.gauge = wx.Gauge(parent=panel, style=wx.GA_HORIZONTAL)
        self.gauge.SetRange(100)
    # -

        self.szr_panel = wx.BoxSizer(wx.VERTICAL)
        self.szr_panel.Add(self.progress_txt, flag=wx.CENTER)
        self.szr_panel.Add(self.gauge, flag=wx.BOTTOM|wx.CENTER|wx.EXPAND, border=5)

        szr_buttons = wx.BoxSizer(wx.HORIZONTAL)
        szr_buttons.Add(self.btn_scan, flag=wx.RIGHT, border=2)
        szr_buttons.Add(self.btn_scan_cancel, flag=wx.RIGHT, border=2)
        szr_buttons.Add(self.btn_close, flag=wx.RIGHT, border=2)

        self.szr_panel.Add(szr_buttons)
        panel.SetSizer(self.szr_panel)

        # --
        self.messages = wx.html.HtmlWindow(parent=self)
        self.messages.SetPage(self._pref.load_html('scan_start'))

        # --

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(titular, flag=wx.LEFT|wx.ALL, border=5)
        sizer.Add(self.messages, 1, flag=wx.EXPAND)
        sizer.Add(panel, flag=wx.ALL|wx.CENTER, border=5)

        self.SetSizer(sizer)

        self.SetMinSize((450, 300))
        self.Center()

        self._scan_message_idx = -1

        Publisher().subscribe(self.updateProgress, 'update')

    def updateProgress(self, msg):
        if isinstance(msg.data, int):
            self.gauge.SetValue(msg.data)
            self.progress_txt.SetLabel('Progreso %s%%' % msg.data)
            self.szr_panel.Layout()
            if self._pref.scan_messages_count() > 0: 
                tmp = int(msg.data / 101. *  self._pref.scan_messages_count())
                if tmp != self._scan_message_idx:
                    self._scan_message_idx = tmp
                    self.messages.SetPage(self._pref.load_scan_message_html(self._scan_message_idx))
        else:
            if msg.data == 'output_ready':
                self.messages.SetPage(self._pref.load_html('scan_end'))
                wx.GetApp().preferences.save_channels_guide(self._scanner.result())

            elif msg.data == 'scan_failed':
                self.messages.SetPage(self._pref.load_html('scan_error'))

    def OnClose(self, evt):
        #self.timer.Stop()
        if not self._scanner.terminated():
            self._scanner.kill()
        self.Close()

    def OnScan(self, evt):
        self._scanner.scan()





