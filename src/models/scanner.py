# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
from threading import Thread
from Queue import Queue

import wx
from wx.lib.pubsub import Publisher

import re

from channel import ChannelsGuide, Channel

class ScannerThread(Thread):
    def __init__(self, *args, **kwargs):
        super(ScannerThread, self).__init__()
        self.freqs_file = kwargs['freqs_file']
        self.output = kwargs['output']

        data = open(self.freqs_file, 'r').read().splitlines()
        self.frequencies = []

        for line in data:
            result = re.findall('^T (\d+) ', line)
            if len(result):
                self.frequencies.append(int(result[0]))

        self.start()

    def run(self):
        self.process = Popen(
            ['scan', '-q', self.freqs_file],
            stdout=PIPE,
            stderr=PIPE
        )

        per = 100.0/len(self.frequencies)
        scan_count = 0

        for line in iter(self.process.stderr.readline, ''):
            if line.startswith('>>>'):
                freq = int(re.findall(' ([\d]+):', line)[0])
                if freq in self.frequencies:
                    del(self.frequencies[self.frequencies.index(freq)])

                    scan_count += 1
                    percent = int(round(scan_count * per))

                    wx.CallAfter(
                        Publisher().sendMessage,
                        'update',
                        percent
                    )


        out, err = self.process.communicate()

        self.output.put(out)

        if self.process.returncode == 0:
            wx.CallAfter(
                Publisher().sendMessage,
                'update',
                'output_ready'
            )

        else:
            wx.CallAfter(
                Publisher().sendMessage,
                'update',
                'scan_failed'
            )


class ChannelsScanner:
    """
    Scan channels using the `scan` program and returns a channels guide.
    """
    def __init__(self, freqs_file):
        self.freqs_file = freqs_file
        self.process = None
        self.guide = None
        self.discovered_channels = Queue(1)

    def scan(self):
        proc = ScannerThread(
            freqs_file=self.freqs_file,
            output=self.discovered_channels
        )

    def kill(self):
        if self.process:
            self.process.kill()

    def terminated(self):
        return self.process is None or self.process.poll() is not None

    def terminatedOk(self):
        return self.process.returncode == 0

    def result(self):
        if self.guide is not None:
            return self.guide

        self.guide = ChannelsGuide()

        dc = self.discovered_channels.get(block=False)

        for line in dc.splitlines():
            params = line.split(":")
            self.guide.addChannel(Channel({
                        'name': params[0].strip(),
                        'frequency': params[1].strip(),
                        'program': params[-1:][0].strip()
                    })
            )

        return self.guide

