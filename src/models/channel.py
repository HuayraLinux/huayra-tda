# -*- coding: utf-8 -*-

class Channel(object):
    def __init__(self, data):
        self.__dict__.update(data)

        self.info = '%s @ %s : %s' % (self.name, self.frequency, self.program)

class ChannelsGuideSerializer:
    def load(self, path, guide):
        with open(path, 'r') as fd:
            for line in fd.readlines():
                params = line.split(':')
                guide.addChannel(Channel({
                    'name': params[0].strip(),
                    'frequency': params[1].strip(),
                    'program': params[2].strip()
                }))

    def save(self, path, guide):
        with  open(path, 'w') as fd:
            for channel in guide.channels():
                fd.write("%s:%s:%s\n" % (channel.name, channel.frequency, channel.program))


class ChannelsGuide(object):
    def __init__(self):
        self._channels = []
        self._current_index = 0
        self._max_index = len(self._channels) - 1

    def channels(self):
        return self._channels

    def current(self):
        if self._current_index >= 0 and self._current_index <= self._max_index:
            return self._channels[self._current_index]
        else:
            return None

    def previous(self):
        tmp = self._current_index - 1
        self._current_index = self._max_index if tmp < 0 else tmp
        
        return self.current()

    def next(self):
        tmp = self._current_index + 1
        self._current_index = 0 if tmp > self._max_index else tmp

        return self.current()

    def addChannel(self, channel):
        self._channels.append(channel)
        self._max_index = len(self._channels) - 1

    def goto(self, channelIndex):
        self._current_index = channelIndex
        return self.current()

    def currentIndex(self):
        return self._current_index
        
