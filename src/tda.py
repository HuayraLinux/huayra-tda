#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import vlc

from channel import ChannelGuide

VIDEO = 'example/video.mp4'

VLC_SETTINGS = [
    '--video-title-show',
    '--video-title-timeout 1',
    '--video-title-position 4',
    '--disable-screensaver',
    '--drop-late-frames',
    '--skip-frames',
    '--overlay',
]

class MainFrame(wx.Frame):
    def __init__(self):
        super(MainFrame, self).__init__(
            parent=None,
            id=-1,
            title=u'Huayra TDA',
        )

        self._guide = wx.GetApp().guide

        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetFields((u'', u'Canal: ', u'Señal: '))

        # Menú archivo
        file_menu = wx.Menu()
        btn_scan = file_menu.Append(id=-1, text=u'Escanear canales')
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT)

            # Submenú desentrelazado
        opt_deinterlace_menu = wx.Menu()
        self.opt_deint_none = opt_deinterlace_menu.AppendRadioItem(id=-1, text=u'Ninguno')
        self.opt_deint_blend = opt_deinterlace_menu.AppendRadioItem(id=-1, text=u'Blend')
        self.opt_deint_linear = opt_deinterlace_menu.AppendRadioItem(id=-1, text=u'Linear')
        self.opt_deint_x = opt_deinterlace_menu.AppendRadioItem(id=-1, text=u'X')

        self.Bind(wx.EVT_MENU, self.OnDeinterlace, self.opt_deint_none)
        self.Bind(wx.EVT_MENU, self.OnDeinterlace, self.opt_deint_blend)
        self.Bind(wx.EVT_MENU, self.OnDeinterlace, self.opt_deint_linear)
        self.Bind(wx.EVT_MENU, self.OnDeinterlace, self.opt_deint_x)

            # Submenú aspecto
        opt_aspect_menu = wx.Menu()
        self.opt_asp_none = opt_aspect_menu.AppendRadioItem(id=-1, text=u'Ninguno')
        self.opt_asp_43 = opt_aspect_menu.AppendRadioItem(id=-1, text=u'4:3')
        self.opt_asp_169 = opt_aspect_menu.AppendRadioItem(id=-1, text=u'16:9')
        self.opt_asp_1610 = opt_aspect_menu.AppendRadioItem(id=-1, text=u'16:10')

        self.Bind(wx.EVT_MENU, self.OnAspect, self.opt_asp_none)
        self.Bind(wx.EVT_MENU, self.OnAspect, self.opt_asp_43)
        self.Bind(wx.EVT_MENU, self.OnAspect, self.opt_asp_169)
        self.Bind(wx.EVT_MENU, self.OnAspect, self.opt_asp_1610)

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
        self.panel_control = wx.Panel(parent=self)
        #self.panel_control.SetBackgroundColour(wx.RED) # Para ver el panel

        # Botones de control
        channel_list = wx.BitmapButton(parent=self.panel_control,
            bitmap=wx.ArtProvider.GetBitmap('gtk-justify-fill')
        )
        channel_up = wx.BitmapButton(parent=self.panel_control,
            bitmap=wx.ArtProvider.GetBitmap(wx.ART_GO_UP),
        )

        channel_down = wx.BitmapButton(parent=self.panel_control,
            bitmap=wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN)
        )
        volume_mute = wx.BitmapButton(parent=self.panel_control,
            bitmap=wx.ArtProvider.GetBitmap('stock_volume-mute')
        )
        self.full_screen = wx.BitmapButton(parent=self.panel_control,
            bitmap=wx.ArtProvider.GetBitmap('view-fullscreen')
        )
        take_picture = wx.BitmapButton(parent=self.panel_control,
            bitmap=wx.ArtProvider.GetBitmap('camera-photo')
        )
        volume_slider = wx.Slider(
            parent=self.panel_control,
            value=0,
            minValue=0,
            maxValue=100,
            size=(100, -1)
        )

        # Tooltips
        channel_list.SetToolTip(wx.ToolTip(u'Lista de canales'))
        channel_up.SetToolTip(wx.ToolTip(u'Subir canal'))
        channel_down.SetToolTip(wx.ToolTip(u'Bajar canal'))
        volume_mute.SetToolTip(wx.ToolTip(u'Silenciar'))
        self.full_screen.SetToolTip(wx.ToolTip(u'Pantalla completa'))
        take_picture.SetToolTip(wx.ToolTip(u'Sacar foto'))

        # Sizers
        szr_control = wx.BoxSizer(wx.HORIZONTAL)
        szr_control.Add(volume_mute, flag=wx.RIGHT, border=2)
        szr_control.Add(volume_slider, flag=wx.TOP, border=6)
        szr_control.Add(take_picture, flag=wx.LEFT|wx.RIGHT, border=2)
        szr_control.Add(self.full_screen, flag=wx.RIGHT, border=2)
        szr_control.Add(channel_list, flag=wx.RIGHT, border=2)
        szr_control.Add(channel_down, flag=wx.RIGHT, border=2)
        szr_control.Add(channel_up, flag=wx.RIGHT, border=2)
        self.panel_control.SetSizer(szr_control)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel_video, 1, flag=wx.EXPAND)
        sizer.Add(self.panel_control, flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=2)
        self.SetSizer(sizer)

        self.SetMinSize((450, 300))
        self.Center()

        # Bindeos
        #self.Bind(wx.EVT_MENU, self.OnTune, btn_scan)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_BUTTON, self.OnChannelUp, channel_up)
        self.Bind(wx.EVT_BUTTON, self.OnChannelDown, channel_down)
        self.Bind(wx.EVT_BUTTON, self.OnToggleFullScreen, self.full_screen)

        # Bindeos de teclas
        self.id_ESC = wx.NewId()
        self.id_LEFT = wx.NewId()
        self.id_RIGHT = wx.NewId()
        self.id_UP = wx.NewId()
        self.id_DOWN = wx.NewId()

        self.Bind(wx.EVT_MENU, self.OnChannelUp, id=self.id_UP)
        self.Bind(wx.EVT_MENU, self.OnChannelDown, id=self.id_DOWN)
        self.Bind(wx.EVT_MENU, self.OnVolumeUp, id=self.id_RIGHT)
        self.Bind(wx.EVT_MENU, self.OnVolumeDown, id=self.id_LEFT)

        self.SetAcceleratorTable(
            wx.AcceleratorTable(
                [
                    (wx.ACCEL_NORMAL,  wx.WXK_ESCAPE, self.id_ESC),
                    (wx.ACCEL_NORMAL,  wx.WXK_LEFT, self.id_LEFT),
                    (wx.ACCEL_NORMAL,  wx.WXK_RIGHT, self.id_RIGHT),
                    (wx.ACCEL_NORMAL,  wx.WXK_UP, self.id_UP),
                    (wx.ACCEL_NORMAL,  wx.WXK_DOWN, self.id_DOWN),
                ]
            )
        )

        self.vlc_instance = vlc.Instance(' '.join(VLC_SETTINGS))
        self.player = self.vlc_instance.media_player_new()
        self.panel_video.SetFocus()

    def OnExit(self, evt):
        self.Close()

    def OnTune(self, channel):
        self.player.stop()

        self.Media = self.vlc_instance.media_new(
            'dvb-t://frequency=%s' % channel.frequency,
            'program=%s'  % channel.program
        )

        self.player.set_media(self.Media)
        self.player.parse()

        title = self.player.get_title() if self.player.get_title() != -1 else channel.name

        self.status_bar.SetStatusText(u'Canal: %s' % title, 1)
        self.player.set_xwindow(self.panel_video.GetHandle())
        self.player.play()

    def OnStop(self, evt):
        self.player.stop()

    def OnToggleFullScreen(self, evt):
        if self.IsFullScreen():
            self.Unbind(wx.EVT_MENU, id=self.id_ESC)

            self.ShowFullScreen(False)
            self.full_screen.SetBitmapLabel(wx.ArtProvider.GetBitmap('view-fullscreen'))
            self.panel_control.Show()

        else:
            self.Bind(wx.EVT_MENU, self.OnToggleFullScreen, id=self.id_ESC)

            self.ShowFullScreen(True)
            self.full_screen.SetBitmapLabel(wx.ArtProvider.GetBitmap('view-restore'))
            self.panel_control.Hide()
            self.panel_video.SetFocus()

    def OnChannelUp(self, evt):
        self.OnTune(self._guide.next())
        print 'subir canal'

    def OnChannelDown(self, evt):
        self.OnTune(self._guide.previous())
        print 'bajar canal'

    def OnVolumeUp(self, evt):
        print 'subir volumen'

    def OnVolumeDown(self, evt):
        print 'bajar volumen'

    def OnDeinterlace(self, evt):
        '''
            Modos de desentrelazado:
                blend, bob, discard, linear, mean, x, yadif, yadif2x
        '''

        if evt.Id == self.opt_deint_none.Id:
            self.player.video_set_deinterlace(None)

        elif evt.Id == self.opt_deint_blend.Id:
            self.player.video_set_deinterlace('blend')

        elif evt.Id == self.opt_deint_linear.Id:
            self.player.video_set_deinterlace('linear')

        elif evt.Id == self.opt_deint_x.Id:
            self.player.video_set_deinterlace('x')

    def OnAspect(self, evt):
        if evt.Id == self.opt_asp_none:
            self.player.video_set_aspect_ratio(None)

        elif evt.Id == self.opt_asp_43:
            self.player.video_set_aspect_ratio('4:3')

        elif evt.Id == self.opt_asp_169:
            self.player.video_set_aspect_ratio('16:9')

        elif evt.Id == self.opt_asp_1610:
            self.player.video_set_aspect_ratio('16:10')


class HuayraTDA(wx.App):
    def __init__(self):
        self.guide = ChannelGuide()
        super(HuayraTDA, self).__init__(redirect=False)

    def OnInit(self):
        self.frame = MainFrame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True


if __name__ == '__main__':
    app = HuayraTDA()
    app.MainLoop()
