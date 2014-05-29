# -*- coding: utf-8 -*-

from PyQt4.QtCore import QObject, SIGNAL

class Player(QObject):
    def __init__(self, channelsGuide):
        QObject.__init__(self)
        self.currentChannelIndex = None
        self.setGuide(channelsGuide)
        self.volume = 50
        self.playing = False

    def gotoChannelUp(self):
        if self.currentChannelIndex is None:
            return
        if self.currentChannelIndex == self.channelsGuide.channelsCount() - 1:
            self.gotoChannel(0)
        else:
            self.gotoChannel(self.currentChannelIndex + 1)

    def gotoChannelDown(self):
        if self.currentChannelIndex is None:
            return
        if self.currentChannelIndex == 0:
            self.gotoChannel(self.channelsGuide.channelsCount() - 1)
        else:
            self.gotoChannel(self.currentChannelIndex - 1)

    def gotoChannel(self, channelIndex):
        if channelIndex < self.channelsGuide.channelsCount():
            self.currentChannelIndex = channelIndex
        if self.currentChannel() is not None:
            print self.currentChannel().info()
        self.emit(SIGNAL("channelChanged"), self.currentChannel())

    def currentChannel(self):
        if self.currentChannelIndex is None:
            return None
        return self.channelsGuide.channel(self.currentChannelIndex)

    def guide(self):
        return self.channelsGuide

    def setGuide(self, guide):
        self.channelsGuide = guide
        self.currentChannelIndex = None
        self.gotoChannel(0)

    def setVolume(self, volume):
        self.volume = volume
        self.emit(SIGNAL("volumeChanged"), self.volume)

    def volumeInc(self):
        volume = self.volume + 5
        if self.volume > 100: self.volume = 100
        self.setVolume(volume)

    def volumeDec(self):
        volume = self.volume - 5
        if self.volume < 0: self.volume = 0
        self.setVolume(volume)

    def stop(self):
        self.playing = False
        self.emit(SIGNAL("stop"))

    def play(self):
        self.playing = True
        self.emit(SIGNAL("play"), self.currentChannel())

