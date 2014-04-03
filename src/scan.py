# -*- coding: utf-8 -*-

from channel import ChannelsGuide
import subprocess

class ChannelsScannerProcess:
    def __init__(self, freqs_file):
        self.process = subprocess.Popen(["scan", freqs_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
    def cancel(self):
        self.process.kill()
        
    def terminated(self):
        return (self.process.poll() is not None)

    def terminatedOk(self):
        return self.process.returncode == 0
    
    def result(self):
        (data, err) = self.process.communicate()
        return data

