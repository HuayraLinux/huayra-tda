# -*- coding: utf-8 -*-

import os
import sys

from PyQt4 import QtCore, QtGui
from Ui_frmPlayer import Ui_frmPlayer
import vlc

class WidgetPlayer(QtGui.QWidget):
    def __init__(self, player):
        QtGui.QWidget.__init__(self)
        self.fullscreen = False
        self.player = player
        self.ui = Ui_frmPlayer()
        self.ui.setupUi(self)

        self.ui.page_3 = QtGui.QWidget()
        self.ui.paginador.addWidget(self.ui.page_3)

        print dir(self.ui.paginador)

        self.videoframe = self.createVideoFrame(self.ui.page_3)
        self.videoframe.resize(250, 250)

        self.createMediaPlayer()

        self.ui.paginador.setCurrentIndex(1)


        def convert_path(ruta_relativa):
            this_dir = os.path.dirname(os.path.abspath(__file__))
            abs_path = os.path.join(this_dir, ruta_relativa)
            return abs_path


        self.cambiar_icono(self.ui.btnChannelUp, "/usr/share/icons/huayra-limbo/scalable/actions/up.svg")
        self.cambiar_icono(self.ui.btnChannelDown, "/usr/share/icons/huayra-limbo/scalable/actions/down.svg")
        self.cambiar_icono(self.ui.btnShowChannelsList, "/usr/share/icons/huayra-limbo/scalable/actions/top.svg")
        self.cambiar_icono(self.ui.btnFullScreen, "/usr/share/icons/huayra-limbo/scalable/actions/view-fullscreen.svg")

        self.ui.lblHuayra.setPixmap(QtGui.QPixmap(convert_path("imagenes/huayra-tda.svg")))
        self.ui.lblVolumen.setPixmap(QtGui.QPixmap(convert_path("imagenes/volumen.svg")))

        self.connect(self.player, QtCore.SIGNAL("channelChanged"), self.watch, QtCore.Qt.QueuedConnection)
        self.connect(self.ui.btnShowChannelsList, QtCore.SIGNAL("clicked()"), self.showHideChannelsList)
        self.connect(self.ui.btnChannelUp, QtCore.SIGNAL("clicked()"), self.channelUp)
        self.connect(self.ui.btnChannelDown, QtCore.SIGNAL("clicked()"), self.channelDown)
        self.connect(self.player, QtCore.SIGNAL("channelChanged"), self.channelChanged, QtCore.Qt.QueuedConnection)
        self.connect(self.ui.sldVolume, QtCore.SIGNAL("valueChanged(int)"), self.setVolume)
        self.connect(self.player, QtCore.SIGNAL("volumeChanged"), self.updateVolume, QtCore.Qt.QueuedConnection)
        self.connect(self.ui.btnFullScreen, QtCore.SIGNAL("clicked()"), self.toggle_fullscreen)
        self.connect(self.player, QtCore.SIGNAL("play"), self.watch, QtCore.Qt.QueuedConnection)
        self.connect(self.player, QtCore.SIGNAL("stop"), self.stop, QtCore.Qt.QueuedConnection)
        self.ui.btnFullScreen.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return))
        self.ui.btnChannelDown.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Down))
        self.ui.btnChannelUp.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Up))
        self.channelsModel = QtGui.QStandardItemModel()
        self.ui.listViewChannels.setModel(self.channelsModel)
        self.connect(self.ui.listViewChannels.selectionModel(),
            QtCore.SIGNAL("currentRowChanged(QModelIndex,QModelIndex)"), self.channelSelectionChanged)
        self.updateChannelsList()
        self.showHideChannelsList()
        self.updateVolume()
        self.i = 0

    def cambiar_icono(self, widget, path):
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(path), QtGui.QIcon.Normal, QtGui.QIcon.On)
        widget.setIcon(icon1)

    def createVideoFrame(self, parent):
        if sys.platform == "darwin": # for MacOS
            videoframe = QtGui.QMacCocoaViewContainer(0)
        else:
            videoframe = QtGui.QFrame(parent)

        palette = videoframe.palette()
        palette.setColor (QtGui.QPalette.Window,
                               QtGui.QColor(0,0,0))
        videoframe.setPalette(palette)
        videoframe.setAutoFillBackground(True)
        videoframe.setFocusPolicy(QtCore.Qt.StrongFocus)
        videoframe.installEventFilter(self)
        return videoframe

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Escape:
                self.toggle_fullscreen()
            if event.key() == QtCore.Qt.Key_Up:
                self.channelUp()
            if event.key() == QtCore.Qt.Key_Down:
                self.channelDown()
            if event.key() == QtCore.Qt.Key_Right:
                self.volumeInc()
            if event.key() == QtCore.Qt.Key_Left:
                self.volumeDec()

        return False

    def showHideChannelsList(self):
        if self.ui.listViewChannels.isHidden():
            self.ui.listViewChannels.show()
        else:
            self.ui.listViewChannels.hide()

    def channelUp(self):
        self.player.gotoChannelUp()

    def channelDown(self):
        self.player.gotoChannelDown()

    def paintEvent(self, pe):
        opt = QtGui.QStyleOption()
        opt.init(self)
        p = QtGui.QPainter(self)
        s = self.style()
        s.drawPrimitive(QtGui.QStyle.PE_Widget, opt, p, self)

    def updateChannelsList(self):
        self.channelsModel.clear()
        for channel in self.player.guide().channels:
            self.channelsModel.appendRow(QtGui.QStandardItem(channel.name))

    def channelSelectionChanged(self, idx1, idx2):
        self.player.gotoChannel(idx1.row())

    def channelChanged(self, channel):
        if channel is not None:
            self.ui.listViewChannels.selectionModel().setCurrentIndex(
                self.channelsModel.index(self.player.currentChannelIndex, 0),
                QtGui.QItemSelectionModel.SelectionFlags()
            )

    def setVolume(self, volume):
        self.player.setVolume(volume)

    def createMediaPlayer(self):
        # creating a basic vlc instance
        self.instance = vlc.Instance("--video-title-show --video-title-timeout 1 --sub-source marq")
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()
        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform == "linux2": # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32": # for Windows
            self.mediaplayer.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin": # for MacOS
            self.mediaplayer.set_nsobject(self.videoframe.winId())
        self.updateVolume()

    def watch(self, channel):
        self.mediaplayer.stop()
        if channel is None:
            return
        self.currentChannel = channel
        # create the media
        self.media = self.instance.media_new('dvb-t://frequency=' + channel.frequency, 'program='+channel.program)
        # put the media in the media player
        self.mediaplayer.set_media(self.media)

        # parse the metadata of the file
        self.media.parse()
        # set the title of the track as window title
        self.setWindowTitle("Huayra TDA Player - " + channel.name)
        self.mediaplayer.play()
        self.mediaplayer.video_set_marquee_int(vlc.VideoMarqueeOption.Position, vlc.Position.Bottom)
        self.mediaplayer.video_set_marquee_int(vlc.VideoMarqueeOption.Timeout, 5*1000)
        self.mediaplayer.video_set_marquee_string(vlc.VideoMarqueeOption.Text, channel.name)

    def setDeinterlace(self, mode='linear'):
        '''
            Modos de desentrelazado:
                blend, bob, discard, linear, mean, x, yadif, yadif2x
        '''
        vlc.libvlc_video_set_deinterlace(self.mediaplayer, mode)

    def setAspect(self, mode='16:9'):
        '''
            Modos de desentrelazado:
                blend, bob, discard, linear, mean, x, yadif, yadif2x
        '''
        vlc.libvlc_video_set_aspect_ratio(self.mediaplayer, mode)

    def updateVolume(self):
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(self.player.volume)
        self.ui.lblVolumenVal.setText(str(self.player.volume) + ' %')
        self.ui.sldVolume.setValue(self.player.volume)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.ui.btnChannelDown.hide()
            self.ui.btnChannelUp.hide()
            self.ui.lblVolumen.hide()
            self.ui.sldVolume.hide()
            self.ui.lblVolumenVal.hide()
            self.ui.btnShowChannelsList.hide()
            self.ui.btnFullScreen.hide()
            self.ui.lblHuayra.hide()
            self.ui.listViewChannels.hide()
            self.emit(QtCore.SIGNAL("fullscreen"), self.fullscreen)
        else:
            self.ui.btnChannelDown.show()
            self.ui.btnChannelUp.show()
            self.ui.lblVolumen.show()
            self.ui.sldVolume.show()
            self.ui.lblVolumenVal.show()
            self.ui.btnShowChannelsList.show()
            self.ui.btnFullScreen.show()
            self.ui.lblHuayra.show()
            self.emit(QtCore.SIGNAL("fullscreen"), self.fullscreen)

    def volumeInc(self):
        self.player.volumeInc()

    def volumeDec(self):
        self.player.volumeDec()

    def stop(self):
        self.mediaplayer.stop()
