# -*- coding: utf-8 -*-


from xdg import BaseDirectory

import ConfigParser
import io
import os.path
import re


class Preferences(object):
    def __init__(self, *args, **kwargs):
        self.user_path = os.path.expanduser('~')

        self._load_pictures_path()

    def _load_pictures_path(self):
        path = os.path.join(BaseDirectory.xdg_config_home, 'user-dirs.dirs')
        with open(path, 'r') as fd:
            user_config = '[XDG_USER_DIR]\n' + fd.read()

        user_config = re.sub('\$HOME', self.user_path, user_config)
        user_config = re.sub('"', '', user_config)

        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.readfp(io.BytesIO(user_config))

        self.pictures_path = config.get('XDG_USER_DIR', 'XDG_PICTURES_DIR')

