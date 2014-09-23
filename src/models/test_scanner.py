# -*- coding: utf-8 -*-

import unittest
import time
from scanner import ChannelsScanner

class TestChannelsScanner(unittest.TestCase):
    def setUp(self):
        pass

    def test_process(self):
        scanner = ChannelsScanner("../isdb-t.txt")
        scanner.scan()
        while not scanner.terminated():
            time.sleep(5)
        self.assertTrue(scanner.terminatedOk(), 'El proceso de scan no devolvio 0')
        channels =  scanner.result().channels()
        self.assertGreater(len(channels) , 0, 'No se encontraron canales')


if __name__ == '__main__':
    unittest.main()
