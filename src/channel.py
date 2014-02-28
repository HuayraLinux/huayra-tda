class Channel:
    def __init__(self, name=None, frequency=None, program=None):
        self.name = name
        self.frequency = frequency
        self.program = program

    def __unicode__(self):
        return self.name

    def info(self):
        return self.name + " @ " + self.frequency + " : " + self.program

class ChannelsGuide:
    def __init__(self):
        self.channels = []

    def addChannel(self, channel):
        self.channels.append(channel)

    def channelsCount(self):
        return len(self.channels)

    def channel(self, channelIndex):
        return self.channels[channelIndex]
