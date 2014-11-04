# -*- coding: utf-8 -*-

from channel import ChannelsGuideSerializer
from xdg import BaseDirectory

import ConfigParser
import io
import os.path
import re
import glob


class Preferences(object):
    def __init__(self, app_path, *args, **kwargs):
        self.app_path = app_path
        self.user_path = os.path.expanduser('~')
        self._load_pictures_path()
        self._scan_messages = glob.glob(os.path.join(self.app_path, 'html', 'scan_messages') + '/*.html')
        self._scan_messages.sort()

    def _load_pictures_path(self):
        path = os.path.join(BaseDirectory.xdg_config_home, 'user-dirs.dirs')
        with open(path, 'r') as fd:
            user_config = '[XDG_USER_DIR]\n' + fd.read()

        user_config = re.sub('\$HOME', self.user_path, user_config)
        user_config = re.sub('"', '', user_config)

        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.readfp(io.BytesIO(user_config))

        self.pictures_path = config.get('XDG_USER_DIR', 'XDG_PICTURES_DIR')

    def load_html(self, html):
        with open(os.path.join(self.app_path, 'html', '%s.html' % html), 'r') as fd:
            data = fd.read()

        data = data.replace("{{ app_path }}", self.app_path)
        return data

    def load_scan_message_html(self, index):
        with open(self._scan_messages[index], 'r') as fd:
            data = fd.read()
        data = data.replace("{{ app_path }}", self.app_path)
        return data

    def scan_messages_count(self):
        return len(self._scan_messages)

    def channels_list_path(self):
        return self.user_path + '/.huayra-tda-channels.conf'

    def load_channels_guide(self, guide):
        serializer = ChannelsGuideSerializer()
        try:
            serializer.load(self.channels_list_path(), guide)
        except IOError as e:
            print e
        return guide

    def save_channels_guide(self, guide):
        serializer = ChannelsGuideSerializer()
        serializer.save(self.channels_list_path(), guide)

    def get_frequencies_file_path(self):
        if os.path.exists('./isdb-t.txt'):
            return os.path.abspath('./isdb-t.txt')
        elif os.path.exists('/etc/huayra-tda-player/isdb-t.txt'):
            return os.path.abspath('/etc/huayra-tda-player/isdb-t.txt')
        raise Exception('Frequencies file does not exist')
         
