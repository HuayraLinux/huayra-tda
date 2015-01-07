# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
from threading import Thread
from Queue import Queue

import wx
from wx.lib.pubsub import pub
import re

class SignalLevelThread(Thread):
    def __init__(self, *args, **kwargs):
        super(SignalLevelThread, self).__init__()
        self._terminate = False
        self.start()

    def run(self):
        self.process = Popen(
            ['femon'],
            stdout=PIPE,
            stderr=PIPE
        )

        for line in iter(self.process.stdout.readline, ''):
            if self._terminate:
                self.process.terminate()
                return
            if line.startswith('status '):
                snr = re.findall('snr ([\dabcdef]+) ', line)[0]
                snr = int(snr, base=16)
                wx.CallAfter(
                    pub.sendMessage,
                    'signalLevelUpdate',
                    level=snr
                )

    def terminate(self):
        self._terminate = True
