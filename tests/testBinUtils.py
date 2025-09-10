#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Unit tests for binUtils module.
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from daptools.binUtils import bytes2bin, bin2bytes, bin2dec, dec2bin, bytes2str


class TestBinUtils(unittest.TestCase):

    def test_bytes2bin(self):
        result = bytes2bin('\x01\x02')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 16)  # 2 bytes * 8 bits

    def test_bin2bytes(self):
        bits = [0, 0, 0, 0, 0, 0, 0, 1]  # Binary for 1
        result = bin2bytes(bits)
        self.assertEqual(ord(result), 1)

    def test_bin2dec(self):
        bits = [0, 0, 0, 0, 0, 0, 0, 1]  # Binary for 1
        result = bin2dec(bits)
        self.assertEqual(result, 1)

    def test_dec2bin(self):
        result = dec2bin(5)
        self.assertEqual(result, [1, 0, 1])  # Binary for 5

    def test_bytes2str(self):
        result = bytes2str('\x01\x02')
        self.assertIn('\\x01', result)
        self.assertIn('\\x02', result)


if __name__ == '__main__':
    unittest.main()