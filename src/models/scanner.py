# -*- coding: utf-8 -*-

from channel import ChannelsGuide, Channel
import subprocess

class ChannelsScanner:
    """
    Scan channels using the `scan` program and returns a channels guide.
    """
    def __init__(self, freqs_file):
        self.freqs_file = freqs_file

    def scan(self):
        self.process = subprocess.Popen(["scan", self.freqs_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.guide = None

    def kill(self):
        self.process.kill()
        
    def terminated(self):
        return (self.process.poll() is not None)

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
                    }))
        return self.guide

