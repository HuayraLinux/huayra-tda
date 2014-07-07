# -*- coding: utf-8 -*-


import os


class Channel(object):
    def __init__(self, data):
        self.__dict__.update(data)

        self.info = '%s @ %s : %s' % (self.name, self.frequency, self.program)


class ChannelGuide(object):
    def __init__(self, *args, **kwargs):
        self._channels = []
        self._load()

    def _load(self):
        with open('~/.channels.conf', 'r') as fd:
            for line in fd.readlines():
                params = line.split(':')
                self._channels.append(Channel({
                    'name': self.name,
                    'frequency': self.frequency,
                    'program': self.program
                }))

    @property
    def channels(self):
        return self._channels


