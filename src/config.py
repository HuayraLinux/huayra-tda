# -*- coding: utf-8 -*-

import os
from channel import Channel

# Canales sin nombres
CANALES = {
    '[e741]': u'TV Pública HD',
    '[e758]': u'TV Pública Movil',
    '[e742]': u'TV Pública SD',
    '[e880]': u'Canal 13 SD',
    '[e881]': u'Canal 13 Prueba',
}

class Config:
    CHANNELS_FILE = '.channels.conf'

    def __init__(self):
        self.path = os.path.join(os.getenv('HOME'), self.CHANNELS_FILE)
        self.no_config = False if os.path.exists(self.path) else True

    def loadChannelsGuide(self, guide):
        if self.no_config:
            return

        f = open(self.path, 'r')
        for line in f.readlines():
            params = line.split(":")

            canal_nombre = CANALES.get(params[0].strip(), params[0].strip())
            canal_frecuencia = params[1].strip()
            canal_id = params[-1:][0].strip() # No sé el nombre de este valor

            channel = Channel(canal_nombre, canal_frecuencia, canal_id)
            guide.addChannel(channel)

    def save(self, txt):
        f = open(self.path, 'w')
        f.write(txt)
        f.close()
