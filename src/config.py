import os
from channel import Channel

class Config:
    CHANNELS_FILE = 'channels.conf'

    def __init__(self):
        self.path = os.getenv('HOME') + '/.huayra-tda/'
        if not os.path.isdir(self.path):
            os.mkdir(self.path, 0700)

    def loadChannelsGuide(self, guide):
        path = self.path + Config.CHANNELS_FILE
        if not os.path.exists(path):
            return
        f = open(path, 'r')
        for line in f.readlines():
            params = line.split(":")            
            channel = Channel(params[0].strip(), params[1].strip(), params[-1:][0].strip())
            guide.addChannel(channel)
