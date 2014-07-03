#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

class MainFrame(wx.Frame):
    def __init__(self):
        super(MainFrame, self).__init__(
            parent=None,
            id=-1,
            title=u'Huayra TDA',
        )

        # Menú archivo
        file_menu = wx.Menu()
        file_menu.Append(1, u'Escanear canales')
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT)

        # Menú opciones
        opt_deinterlace_menu = wx.Menu()
        opt_deinterlace_menu.AppendRadioItem(id=-1, text=u'Ninguno')
        opt_deinterlace_menu.AppendRadioItem(id=-1, text=u'Blend')
        opt_deinterlace_menu.AppendRadioItem(id=-1, text=u'Linear')
        opt_deinterlace_menu.AppendRadioItem(id=-1, text=u'X')

        opt_aspect_menu = wx.Menu()
        opt_aspect_menu.AppendRadioItem(id=-1, text=u'Ninguno')
        opt_aspect_menu.AppendRadioItem(id=-1, text=u'4:3')
        opt_aspect_menu.AppendRadioItem(id=-1, text=u'16:9')
        opt_aspect_menu.AppendRadioItem(id=-1, text=u'16:10')

        options_menu = wx.Menu()
        options_menu.AppendSubMenu(opt_deinterlace_menu, 'Desentrelazado')
        options_menu.AppendSubMenu(opt_aspect_menu, 'Aspecto')

        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, u'Archivo')
        menu_bar.Append(options_menu, u'Opciones')

        self.SetMenuBar(menu_bar)

        # Paneles
        # Panel de reproductor
        self.video_panel = wx.Panel(parent=self, id=-1)
        self.video_panel.SetBackgroundColour(wx.RED)

        # Panel de control
        control_panel = wx.Panel(parent=self)
        pause = wx.Button(control_panel, label="Pause")

        # Sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        box_control = wx.BoxSizer(wx.HORIZONTAL)

        box_control.Add(control_panel)

        sizer.Add(self.video_panel, flag=wx.EXPAND)
        sizer.Add(box_control, flag=wx.EXPAND)

        self.SetSizer(sizer)
        self.SetMinSize((350, 300))

        # Bindeos
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)

        self.Center()

    def OnExit(self, evt):
        self.Close()


class HuayraTDA(wx.App):
    def __init__(self):
        super(HuayraTDA, self).__init__(redirect=False)

    def OnInit(self):
        self.frame = MainFrame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True


if __name__ == '__main__':
    app = HuayraTDA()
    app.MainLoop()
