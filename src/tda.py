#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import vlc
import os.path

from models.audio import Volume
from models.channel import ChannelsGuide
from models.scanner import ChannelsScanner
from models.preferences import Preferences
from models.signal_level import SignalLevelThread

from views.scan import ChannelScan
from views.about import AboutDialog

from wx.lib.pubsub import pub
import atexit

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

        self._pref= wx.GetApp().preferences
        self._guide = wx.GetApp().guide
        self._volume= wx.GetApp().volume
        self._scan_screen = None
        self._about_screen = None

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.HidePanel, self.timer)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetFields((u'', u'Canal: ', u'SNR: '))

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

        self.Bind(wx.EVT_MENU, self.OnScan, btn_scan)

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
        
        # Menú archivo
        help_menu = wx.Menu()
        btn_about = help_menu.Append(id=-1, text=u'Acerca de...')
        self.Bind(wx.EVT_MENU, self.OnAbout, btn_about)

        # Asignación de Menú
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, u'Archivo')
        menu_bar.Append(options_menu, u'Opciones')
        menu_bar.Append(help_menu, u'Ayuda')
        self.SetMenuBar(menu_bar)

        # Panel de video
        self.panel_video = wx.Panel(parent=self)
        self.panel_video.SetBackgroundColour(wx.BLACK)
        self.panel_video.Bind(wx.EVT_LEFT_DCLICK, self.OnToggleFullScreen)

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
        self.volume_mute = wx.BitmapButton(parent=self.panel_control,
            bitmap=wx.ArtProvider.GetBitmap('stock_volume-med')
        )
        self.full_screen = wx.BitmapButton(parent=self.panel_control,
            bitmap=wx.ArtProvider.GetBitmap('view-fullscreen')
        )
        take_picture = wx.BitmapButton(parent=self.panel_control,
            bitmap=wx.ArtProvider.GetBitmap('camera-photo')
        )
        self.volume_slider = wx.Slider(
            parent=self.panel_control,
            value=50,
            minValue=0,
            maxValue=100,
            size=(100, -1)
        )

        self.volume_slider.Bind(wx.EVT_SCROLL, self.OnVolumeChange)

        # Tooltips
        channel_list.SetToolTip(wx.ToolTip(u'Lista de canales'))
        channel_up.SetToolTip(wx.ToolTip(u'Subir canal'))
        channel_down.SetToolTip(wx.ToolTip(u'Bajar canal'))
        self.volume_mute.SetToolTip(wx.ToolTip(u'Silenciar'))
        self.full_screen.SetToolTip(wx.ToolTip(u'Pantalla completa'))
        take_picture.SetToolTip(wx.ToolTip(u'Sacar foto'))

        # Sizers
        szr_control = wx.BoxSizer(wx.HORIZONTAL)
        szr_control.Add(self.volume_mute, flag=wx.RIGHT, border=2)
        szr_control.Add(self.volume_slider, flag=wx.TOP, border=6)
        szr_control.Add(take_picture, flag=wx.LEFT|wx.RIGHT, border=2)
        szr_control.Add(self.full_screen, flag=wx.RIGHT, border=2)
        szr_control.Add(channel_list, flag=wx.RIGHT, border=2)
        szr_control.Add(channel_down, flag=wx.RIGHT, border=2)
        szr_control.Add(channel_up, flag=wx.RIGHT, border=2)
        self.panel_control.SetSizer(szr_control)
        
        self.channels_list_box = wx.ListBox(choices=[], name='channelsListBox', parent=self)
        self.Bind(wx.EVT_LISTBOX, self.OnChannelsListBox, self.channels_list_box)

        self.updateChannelsList()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_video, 4, flag=wx.EXPAND)
        self.sizer.Add(self.panel_control, flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=2)
        self.sizer.Add(self.channels_list_box, 1, flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=2)
        self.SetSizer(self.sizer)

        self.SetMinSize((450, 300))
        self.Center()

        # Bindeos
        #self.Bind(wx.EVT_MENU, self.OnTune, btn_scan)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_BUTTON, self.OnChannelUp, channel_up)
        self.Bind(wx.EVT_BUTTON, self.OnChannelDown, channel_down)
        self.Bind(wx.EVT_BUTTON, self.OnToggleFullScreen, self.full_screen)
        self.Bind(wx.EVT_BUTTON, self.OnShowChannelsList, channel_list)
        
        take_picture.Bind(wx.EVT_BUTTON, self.OnSnapshot)
        self.volume_mute.Bind(wx.EVT_BUTTON, self.OnMute)

        # Bindeos de teclas
        self.id_ESC = wx.NewId()
        self.id_LEFT = wx.NewId()
        self.id_RIGHT = wx.NewId()
        self.id_UP = wx.NewId()
        self.id_DOWN = wx.NewId()
        self.id_M = wx.NewId()

        self.Bind(wx.EVT_MENU, self.OnChannelUp, id=self.id_UP)
        self.Bind(wx.EVT_MENU, self.OnChannelDown, id=self.id_DOWN)
        self.Bind(wx.EVT_MENU, self.OnVolumeUp, id=self.id_RIGHT)
        self.Bind(wx.EVT_MENU, self.OnVolumeDown, id=self.id_LEFT)
        self.Bind(wx.EVT_MENU, self.OnMute, id=self.id_M)

        self.SetAcceleratorTable(
            wx.AcceleratorTable(
                [
                    (wx.ACCEL_NORMAL,  wx.WXK_ESCAPE, self.id_ESC),
                    (wx.ACCEL_NORMAL,  wx.WXK_LEFT, self.id_LEFT),
                    (wx.ACCEL_NORMAL,  wx.WXK_RIGHT, self.id_RIGHT),
                    (wx.ACCEL_NORMAL,  wx.WXK_UP, self.id_UP),
                    (wx.ACCEL_NORMAL,  wx.WXK_DOWN, self.id_DOWN),
                    (wx.ACCEL_NORMAL,  ord('m'), self.id_M),
                ]
            )
        )

        self.vlc_instance = vlc.Instance(' '.join(VLC_SETTINGS))
        self.player = self.vlc_instance.media_player_new()
        self.panel_video.SetFocus()

        self.vlc_events = self.player.event_manager()
        self.vlc_events.event_attach(
            vlc.EventType.MediaPlayerOpening,
            self.test
        )

        self.vlc_events.event_attach(
            vlc.EventType.MediaPlayerPlaying,
            self.test1
        )
        self.delay_start_timer = wx.Timer()
        self.delay_start_timer.Bind(wx.EVT_TIMER, self.OnStartTimer)
        self.delay_start_timer.Start(1000, oneShot = wx.TIMER_ONE_SHOT)
        self.signal_level_thread = SignalLevelThread()
        atexit.register(self.signal_level_thread.terminate)
        pub.subscribe(self.signalLevelUpdate, 'signalLevelUpdate')


    def signalLevelUpdate(self, level):
        self.status_bar.SetStatusText(u'SNR: ' + str(level), 2)

    def OnStartTimer(self, evt):
        if self._guide.current() is None:
            # No hay canales
            self.OnScan()
        else:
            self.OnTune(self._guide.current())

    def test(self, evt):
        print 'Sintonizando'

    def test1(self, evt):
        print 'Reproduciendo'

    def OnScan(self, evt=None):
        self.player.stop()
        if self._scan_screen is None:
            self._scan_screen = ChannelScan(wx.GetApp().scanner, parent=self)
            self._scan_screen.Bind(wx.EVT_CLOSE, self.OnScanClose)
        self._scan_screen.Show()
    
    def OnAbout(self, evt=None):
        self._about_screen = AboutDialog(parent=self)
        self._about_screen.Show()
    
    def updateChannelsList(self):
        self.channels_list_box.Clear()
        for channel in self._guide.channels():
            self.channels_list_box.Append(channel.name)

    def OnScanClose(self, evt):
        self._scan_screen = None
        self._guide = ChannelsGuide()
        self._pref.load_channels_guide(self._guide)
        self.updateChannelsList()
        self.OnTune(self._guide.current())
        evt.Skip()

    def OnExit(self, evt):
        self.Close()

    def OnTune(self, channel):
        self.player.set_xwindow(self.panel_video.GetHandle())
        self.player.stop()

        if channel is None:
            self.status_bar.SetStatusText(u'Sin canales', 1)
            return

        self.Media = self.vlc_instance.media_new(
            'dvb-t://frequency=%s' % channel.frequency,
            'program=%s'  % channel.program
        )

        self.player.set_media(self.Media)

        title = self.player.get_title() if self.player.get_title() != -1 else channel.name

        self.status_bar.SetStatusText(u'Canal: %s' % title, 1)
        self.player.play()
        self.channels_list_box.SetSelection(self._guide.currentIndex())
        self.channels_list_box.EnsureVisible(self._guide.currentIndex())


    def OnVolume(self):
        self.player.audio_set_volume(self._volume.current)
        self.volume_slider.SetValue(self._volume.current)

    def OnStop(self, evt):
        self.player.stop()

    def OnToggleFullScreen(self, evt):
        if self.IsFullScreen():
            self.timer.Stop()
            self.Unbind(wx.EVT_MENU, id=self.id_ESC)
            self.panel_video.Unbind(wx.EVT_MOTION)

            self.ShowFullScreen(False)
            self.full_screen.SetBitmapLabel(wx.ArtProvider.GetBitmap('view-fullscreen'))
            self.panel_control.Show()
        else:
            self.Bind(wx.EVT_MENU, self.OnToggleFullScreen, id=self.id_ESC)
            self.panel_video.Bind(wx.EVT_MOTION, self.OnMouseMove)

            self.ShowFullScreen(True)
            self.full_screen.SetBitmapLabel(wx.ArtProvider.GetBitmap('view-restore'))
            self.panel_control.Hide()
            self.channels_list_box.Hide()
            self.panel_video.SetFocus()
        self.sizer.Layout()

    def OnChannelUp(self, evt):
        self.OnTune(self._guide.next())

    def OnChannelDown(self, evt):
        self.OnTune(self._guide.previous())

    def OnVolumeUp(self, evt):
        self._volume.up()
        self.OnVolume()

    def OnVolumeDown(self, evt):
        self._volume.down()
        self.OnVolume()

    def OnVolumeChange(self, evt):
        self._volume.current = self.volume_slider.GetValue()
        self.OnVolume()

    def OnMute(self, evt):
        if self.player.audio_get_mute() == 0:
            self.player.audio_set_mute(True)
            self.volume_mute.SetBitmapLabel(wx.ArtProvider.GetBitmap('stock_volume-mute'))

        else:
            self.player.audio_set_mute(False)
            self.volume_mute.SetBitmapLabel(wx.ArtProvider.GetBitmap('stock_volume-med'))


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
        if evt.Id == self.opt_asp_none.Id:
            self.player.video_set_aspect_ratio(None)

        elif evt.Id == self.opt_asp_43.Id:
            self.player.video_set_aspect_ratio('4:3')

        elif evt.Id == self.opt_asp_169.Id:
            self.player.video_set_aspect_ratio('16:9')

        elif evt.Id == self.opt_asp_1610.Id:
            self.player.video_set_aspect_ratio('16:10')

    def OnSnapshot(self, evt):
        self.player.video_take_snapshot(0, self._pref.pictures_path, 0, 0)

    def OnMouseMove(self, evt):
        pc_w, pc_h = self.panel_control.GetSize()
        pv_w, pv_h = self.panel_video.GetSize()

        x = (pv_w / 2) - (pc_w / 2)
        y = pv_h - (2 * pc_h)

        #self.panel_control.SetPosition((x, y))
        self.panel_control.Show()
        self.sizer.Layout()
        self.timer.Start(5000)

    def HidePanel(self, evt):
        self.timer.Stop()
        self.panel_control.Hide()
        self.channels_list_box.Hide()
        self.sizer.Layout()

    def OnShowChannelsList(self, evt):
        if self.channels_list_box.IsShown():
            self.channels_list_box.Hide()
        else:
            self.channels_list_box.Show()
        self.sizer.Layout()

    def OnChannelsListBox(self, evt):
        selection = self.channels_list_box.GetSelections()
        if len(selection) > 0:
            self.OnTune(self._guide.goto(selection[0]))

    def OnClose(self, evt):
        self.player.stop()
        self.signal_level_thread.terminate()
        self.Destroy()


class HuayraTDA(wx.App):
    def __init__(self):
        self.preferences = Preferences(os.path.dirname(os.path.realpath(__file__)))
        self.guide = ChannelsGuide()
        self.preferences.load_channels_guide(self.guide)
        self.scanner = ChannelsScanner(self.preferences.get_frequencies_file_path())
        self.volume = Volume()

        super(HuayraTDA, self).__init__(redirect=False)

    def OnInit(self):
        self.frame = MainFrame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True


if __name__ == '__main__':
    import subprocess

    cmd = ['mate-screensaver-command', '-i']
    proc = subprocess.Popen(cmd)
    atexit.register(proc.terminate)
    pid = proc.pid

    app = HuayraTDA()
    app.MainLoop()
