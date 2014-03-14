from PyQt4 import QtCore, QtGui
from Ui_frmPlayer import Ui_frmPlayer
import sys
import vlc

class WidgetPlayer(QtGui.QWidget):
    def __init__(self, player):
        QtGui.QWidget.__init__(self)
        self.player = player
        self.ui = Ui_frmPlayer()
        self.ui.setupUi(self)
        self.videoframe = self.createVideoFrame()
        self.createMediaPlayer()
        self.ui.layoutVideo.addWidget(self.videoframe)
        self.connect(self.player, QtCore.SIGNAL("channelChanged"), self.watch, QtCore.Qt.QueuedConnection)
        self.connect(self.ui.btnShowChannelsList, QtCore.SIGNAL("clicked()"), self.showHideChannelsList)
        self.connect(self.ui.btnChannelUp, QtCore.SIGNAL("clicked()"), self.channelUp)
        self.connect(self.ui.btnChannelDown, QtCore.SIGNAL("clicked()"), self.channelDown)
        self.connect(self.player, QtCore.SIGNAL("channelChanged"), self.channelChanged, QtCore.Qt.QueuedConnection)
        self.connect(self.ui.sldVolume, QtCore.SIGNAL("valueChanged(int)"), self.setVolume)
        self.connect(self.player, QtCore.SIGNAL("volumeChanged"), self.updateVolume, QtCore.Qt.QueuedConnection)
        self.connect(self.ui.btnFullScreen, QtCore.SIGNAL("clicked()"), self.fullscreen)
        self.channelsModel = QtGui.QStandardItemModel()
        self.ui.listViewChannels.setModel(self.channelsModel)
        self.connect(self.ui.listViewChannels.selectionModel(), 
            QtCore.SIGNAL("currentRowChanged(QModelIndex,QModelIndex)"), self.channelSelectionChanged)
        self.updateChannelsList()
        self.showHideChannelsList()
        self.updateVolume()

    def createVideoFrame(self):
        if sys.platform == "darwin": # for MacOS
            videoframe = QtGui.QMacCocoaViewContainer(0)
        else:
            videoframe = QtGui.QFrame()
        palette = videoframe.palette()
        palette.setColor (QtGui.QPalette.Window,
                               QtGui.QColor(0,0,0))
        videoframe.setPalette(palette)
        videoframe.setAutoFillBackground(True)
        return videoframe

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
        for channel in self.player.guide().channels:
            self.channelsModel.appendRow(QtGui.QStandardItem(channel.name))

    def channelSelectionChanged(self, idx1, idx2):
        self.player.gotoChannel(idx1.row())

    def channelChanged(self, channel):
#        self.ui.listViewChannels.selectionModel().setCurrentIndex(
#            self.channelsModel.index(self.player.currentChannelIndex, 0),
#            QtGui.QItemSelectionModel.SelectionFlags()
#        )
        pass

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
        
    def updateVolume(self):
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(self.player.volume)
        self.ui.lblVolumenVal.setText(str(self.player.volume) + ' %')
        self.ui.sldVolume.setValue(self.player.volume)

    def fullscreen(self):
        return        
        self.fullframe = self.createVideoFrame()
        self.mediaplayer.set_xwindow(self.fullframe.winId())    
        #self.mediaplayer.set_fullscreen(True)
        self.fullframe.showFullScreen()
        
#        self.mediaplayer.toggle_fullscreen()
