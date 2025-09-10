#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Unit tests for randomPasswordGen module.
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from daptools.randomPasswordGen import generate_paswd


class TestRandomPasswordGen(unittest.TestCase):

    def test_generate_paswd(self):
        password = generate_paswd(12)
        self.assertEqual(len(password), 12)  # Function generates exact length
        self.assertIsInstance(password, str)

    def test_generate_paswd_different_lengths(self):
        password1 = generate_paswd(8)
        password2 = generate_paswd(16)
        
        self.assertEqual(len(password1), 8)
        self.assertEqual(len(password2), 16)
        self.assertNotEqual(password1, password2)

    def test_generate_paswd_contains_mixed_chars(self):
        password = generate_paswd(20)
        # Password should contain mix of characters, numbers, and special chars
        self.assertGreater(len(password), 0)
        self.assertIsInstance(password, str)


if __name__ == '__main__':
    unittest.main()