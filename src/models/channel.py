# -*- coding: utf-8 -*-


import os


class Channel(object):
    def __init__(self, data):
        self.__dict__.update(data)

        self.info = '%s @ %s : %s' % (self.name, self.frequency, self.program)


class ChannelGuide(object):
    def __init__(self, pref, *args, **kwargs):
        self._pref = pref

        self._channels = []
        self._path = os.path.join(self._pref.user_path, '.channels.conf')

        self._load()

        self._current_index = 0
        self._max_index = len(self._channels) - 1

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

    def previous(self):
        tmp = self._current_index - 1
        self._current_index = self._max_index if tmp < 0 else tmp

        return self._channels[self._current_index]

    def next(self):
        tmp = self._current_index + 1
        self._current_index = 0 if tmp > self._max_index else tmp

        return self._channels[self._current_index]

