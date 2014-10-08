# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
from threading import Thread

from channel import ChannelsGuide, Channel

class ScannerThread(Thread):
    def __ini__(self, *args, **kwargs):
        super(ScannerThread, self).__init__(*args, **kwargs)
        self.start()

    def run(self):
        pass


class ChannelsScanner:
    """
    Scan channels using the `scan` program and returns a channels guide.
    """
    def __init__(self, freqs_file):
        self.freqs_file = freqs_file
        self.process = None

    def scan(self):
        self.guide = None
        self.process = subprocess.Popen(
            ['scan', '-q', self.freqs_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
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
        (data, err) = self.process.communicate()

        for line in data.splitlines():
            params = line.split(":")
            self.guide.addChannel(Channel({
                        'name': params[0].strip(),
                        'frequency': params[1].strip(),
                        'program': params[-1:][0].strip()
                    })
            )

        return self.guide

