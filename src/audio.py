# -*- coding: utf-8 -*-


class Volume(object):
    def __init__(self, *args, **kwargs):
        self._step = kwargs.get('step', 10)

        self._min = 0
        self._max = 100
        self._current = 50

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, value):
        self._current = value

    def down(self):
        tmp = self._current - (1 * self._step)
        self._current = self._min if tmp < 0 else tmp

    def up(self):
        tmp = self._current + (1 * self._step)
        self._current = self._max if tmp > self._max else tmp

