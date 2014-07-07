# -*- coding: utf-8 -*-


import os


class Channel(object):
    def __init__(self, data):
        self.__dict__.update(data)

        self.info = '%s @ %s : %s' % (self.name, self.frequency, self.program)


class ChannelGuide(object):
    def __init__(self, *args, **kwargs):
        self._channels = []
        self._path = os.path.join(os.getenv('HOME'), 'channels.conf')

        self._load()

    def _load(self):
        with open(self._path, 'r') as fd:
            for line in fd.readlines():
                params = line.split(':')

                self._channels.append(Channel({
                    'name': params[0].strip(),
                    'frequency': params[1].strip(),
                    'program': params[-1:][0].strip()
                }))

    @property
    def channels(self):
        return self._channels


