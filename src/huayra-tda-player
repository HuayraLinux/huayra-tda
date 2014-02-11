#! /usr/bin/python

#
# Huayra TDA Player
# Copyright (C) 2014-2014 Huayra GNU Linux
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
#

import sys
import user
import vlc
from PyQt4 import QtGui, QtCore

class HuayraTDAPlayer(QtGui.QMainWindow):
    """TDA Player
    """
    def __init__(self, master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setWindowTitle("Huayra TDA Player")

        # creating a basic vlc instance
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()

        self.createUI()
        self.channels = self.readChannelsList("/etc/huayra/channels.conf")
        self.currentChannel = 0

    def readChannelsList(self, path):
        try:
            f = open(path, 'r')
            return f.readlines()
        except:
            return []

    def createUI(self):
        """Set up the user interface, signals & slots
        """
        self.widget = QtGui.QWidget(self)
        self.setCentralWidget(self.widget)

        # In this widget, the video will be drawn
        if sys.platform == "darwin": # for MacOS
            self.videoframe = QtGui.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtGui.QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor (QtGui.QPalette.Window,
                               QtGui.QColor(0,0,0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        self.hbuttonbox = QtGui.QHBoxLayout()
        
        self.channelUpBtn = QtGui.QPushButton("+")
        self.hbuttonbox.addWidget(self.channelUpBtn)
        self.connect(self.channelUpBtn, QtCore.SIGNAL("clicked()"),
                     self.ChannelUp)

        self.channelDownBtn = QtGui.QPushButton("-")
        self.hbuttonbox.addWidget(self.channelDownBtn)
        self.connect(self.channelDownBtn, QtCore.SIGNAL("clicked()"),
                     self.ChannelDown)

        self.hbuttonbox.addStretch(1)
        self.volumeslider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.volumeslider.setMaximum(100)
        self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        self.volumeslider.setToolTip("Volume")
        self.hbuttonbox.addWidget(self.volumeslider)
        self.connect(self.volumeslider,
                     QtCore.SIGNAL("valueChanged(int)"),
                     self.setVolume)

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.addLayout(self.hbuttonbox)

        self.widget.setLayout(self.vboxlayout)

        #scan = QtGui.QAction("&Scan Channels", self)
        #self.connect(scan, QtCore.SIGNAL("triggered()"), self.ScanChannels)
        exit = QtGui.QAction("&Salir", self)
        self.connect(exit, QtCore.SIGNAL("triggered()"), sys.exit)
        menubar = self.menuBar()
        filemenu = menubar.addMenu("&Archivo")
        #filemenu.addAction(scan)  
        filemenu.addSeparator()
        filemenu.addAction(exit)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"),
                     self.updateUI)

    def ChannelUp(self):
        if self.currentChannel == len(self.channels) - 1:
            self.watch(0)
        else:
        	self.watch(self.currentChannel + 1)

    def ChannelDown(self):
        if self.currentChannel == 0:
            self.watch(len(self.channels) - 1)
        else:
        	self.watch(self.currentChannel - 1)

    def watch(self, channel):
        self.mediaplayer.stop()
        self.currentChannel = channel
        # create the media
        params = self.channels[channel].split(":")
        self.media = self.instance.media_new('dvb-t://frequency=' + params[1].strip(), 'program='+params[-1:][0].strip())
        # put the media in the media player
        self.mediaplayer.set_media(self.media)

        # parse the metadata of the file
        self.media.parse()
        # set the title of the track as window title
        self.setWindowTitle("Huayra TDA Player - " + params[0].strip())

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
        self.mediaplayer.play()

    def setVolume(self, Volume):
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(Volume)

    def updateUI(self):
        """updates the user interface"""
        pass

    def ScanChannels(self, filename=None):
        """Scan channels and create channels list: not yet implemented
        """
        return

    def start(self):
        if len(self.channels) > 0:
            self.watch(0)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    player = HuayraTDAPlayer()
    player.show()
    player.resize(640, 480)
    #if sys.argv[1:]:
    player.start()
    sys.exit(app.exec_())
