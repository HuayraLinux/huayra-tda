import tempfile
import os
import unittest
from channel import Channel, ChannelsGuide, ChannelsGuideSerializer

class TestChannelsScanner(unittest.TestCase):
    def setUp(self):
        self.test_data = [
            {
                'name': 'My Chan',
                'frequency': '9894032',
                'program': '2'
            },
            {
                'name': 'Other',
                'frequency': '323123334',
                'program': '5'
            },
            {
                'name': 'Cocos TV',
                'frequency': '987654120',
                'program': '12'
            }
        ]

    def test_load(self):
        guide = ChannelsGuide()
        serializer = ChannelsGuideSerializer()
        (fd, path) = tempfile.mkstemp()
        os.close(fd)
        with open(path, 'w') as fd:
            for chan in self.test_data:
                fd.write("%s:%s:%s\n" % (chan['name'], chan['frequency'], chan['program']))
        serializer.load(path, guide)
        idx = 0
        for chan in guide.channels():
            self.assertEqual("%s:%s:%s" % (chan.name, chan.frequency, chan.program), "%s:%s:%s" % (self.test_data[idx]['name'], self.test_data[idx]['frequency'], self.test_data[idx]['program']), 'Datos del canal no coinciden con los guardados: %s' % (chan.name))
            idx += 1
        self.assertEqual(idx, len(self.test_data), 'La cantidad de canales leidos no coincide con los guardados')
        os.unlink(path)

    def test_save(self):
        guide = ChannelsGuide()
        for chan_data in self.test_data:
            guide.addChannel(Channel(chan_data))
        serializer = ChannelsGuideSerializer()
        (fd, path) = tempfile.mkstemp()
        os.close(fd)
        serializer.save(path, guide)
        with open(path, 'r') as fd:
            idx = 0
            for line in fd.readlines():
                self.assertEqual(line, "%s:%s:%s\n" % (self.test_data[idx]['name'], self.test_data[idx]['frequency'], self.test_data[idx]['program']), 'Datos del canal no coinciden con los guardados: %s' % (line))
                idx += 1
            self.assertEqual(idx, len(self.test_data), 'La cantidad de canales leidos no coincide con los guardados')
        os.unlink(path)


if __name__ == '__main__':
    unittest.main()
