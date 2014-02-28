from PyQt4.QtCore import QObject, SIGNAL

class Player(QObject):
    def __init__(self, channelsGuide):
        QObject.__init__(self)
        self.currentChannelIndex = None
        self.setGuide(channelsGuide)

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
        self.gotoChannel(0)
