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

        self.status_bar = self.CreateStatusBar()

        # Menú archivo
        file_menu = wx.Menu()
        file_menu.Append(id=-1, text=u'Escanear canales')
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT)

            # Submenú desentrelazado
        opt_deinterlace_menu = wx.Menu()
        opt_deinterlace_menu.AppendRadioItem(id=-1, text=u'Ninguno')
        opt_deinterlace_menu.AppendRadioItem(id=-1, text=u'Blend')
        opt_deinterlace_menu.AppendRadioItem(id=-1, text=u'Linear')
        opt_deinterlace_menu.AppendRadioItem(id=-1, text=u'X')

            # Submenú aspecto
        opt_aspect_menu = wx.Menu()
        opt_aspect_menu.AppendRadioItem(id=-1, text=u'Ninguno')
        opt_aspect_menu.AppendRadioItem(id=-1, text=u'4:3')
        opt_aspect_menu.AppendRadioItem(id=-1, text=u'16:9')
        opt_aspect_menu.AppendRadioItem(id=-1, text=u'16:10')

        # Menú opciones
        options_menu = wx.Menu()
        options_menu.AppendSubMenu(opt_deinterlace_menu, 'Desentrelazado')
        options_menu.AppendSubMenu(opt_aspect_menu, 'Aspecto')

        # Asignación de Menú
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, u'Archivo')
        menu_bar.Append(options_menu, u'Opciones')
        self.SetMenuBar(menu_bar)

        # Panel de video
        self.panel_video = wx.Panel(parent=self)
        self.panel_video.SetBackgroundColour(wx.BLACK)

        # Panel de control
        panel_control = wx.Panel(parent=self)
        panel_control.SetBackgroundColour(wx.RED)

        # Botones de control
        channel_up = wx.Button(parent=panel_control, label=u'Subir canal')
        channel_down = wx.Button(parent=panel_control, label=u'Bajar canal')
        volume_mute = wx.Button(parent=panel_control, label=u'Silencio')
        take_picture = wx.Button(parent=panel_control, label=u'Foto')

        szr_control = wx.BoxSizer(wx.HORIZONTAL)
        szr_control.Add(channel_down, flag=wx.RIGHT, border=2)
        szr_control.Add(channel_up, flag=wx.RIGHT, border=2)
        szr_control.Add(volume_mute, flag=wx.RIGHT, border=2)
        szr_control.Add(take_picture, flag=wx.RIGHT, border=2)
        panel_control.SetSizer(szr_control)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel_video, 1, flag=wx.EXPAND)
        sizer.Add(panel_control, flag=wx.EXPAND|wx.TOP, border=2)
        self.SetSizer(sizer)



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
