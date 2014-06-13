# -*- coding: utf-8 -*-

import os
from channel import Channel

# Canales sin nombres
CANALES = {
    '[e741]': 'TV Pública HD',
    '[e758]': 'TV Pública SD',
    '[e742]': 'TV Pública Móvil',
}

class Config:
    CHANNELS_FILE = '.channels.conf'

    def __init__(self):
        self.path = os.getenv('HOME') + '/'

    def loadChannelsGuide(self, guide):
        path = self.path + Config.CHANNELS_FILE
        if not os.path.exists(path):
            return
        f = open(path, 'r')
        for line in f.readlines():
            params = line.split(":")

            canal_nombre = CANALES.get(params[0].strip(), params[0].strip())
            canal_frecuencia = params[1].strip()
            canal_id = params[-1:][0].strip() # No sé el nombre de este valor

            channel = Channel(canal_nombre, canal_frecuencia, canal_id)
            guide.addChannel(channel)

        raise

    def save(self, txt):
        path = self.path + Config.CHANNELS_FILE
        f = open(path, 'w')
        f.write(txt)
        f.close()
