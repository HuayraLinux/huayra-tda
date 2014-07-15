# -*- coding: utf-8 -*-


import os


class Volume(object):
    def __init__(self, *args, **kwargs):
        self._step = kwargs.get('step', 10)

        self._min = 0
        self._max = 100
        self._current = 50

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
    def current(self):
        return self._current

    @current.setter
    def current(self, value):
        self._current = value

    def down(self):
        tmp = self._current - (1 * self._step)
        self._current = self._min if tmp < 0 else tmp

        return self.current

    def up(self):
        tmp = self._current + (1 * self._step)
        self._current = self._max if tmp > self._max else tmp

        return self.current



