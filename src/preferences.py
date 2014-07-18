# -*- coding: utf-8 -*-


import os.path


class Preferences(object):
    def __init__(self, *args, **kwargs):
        self.user_path = os.path.expanduser('~')
        self.picture_path = os.path.join(self.user_path, 'Imágenes')
