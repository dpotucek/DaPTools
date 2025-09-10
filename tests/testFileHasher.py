#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Unit tests for fileHasher module.
"""

import unittest
import tempfile
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from daptools.fileHasher import strip_first_alphanumeric, hash_names, remove_numbers_from_files


class TestFileHasher(unittest.TestCase):

    def test_strip_first_alphanumeric(self):
        result = strip_first_alphanumeric('123-test_file.txt')
        self.assertEqual(result, 'test_file.txt')
        
        result = strip_first_alphanumeric('001-song.mp3')
        self.assertEqual(result, 'song.mp3')

    def test_hash_names(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = os.path.join(tmpdir, 'test1.txt')
            
            open(file1, 'w').close()
            
            result = hash_names([file1], randomize=0)
            self.assertIsInstance(result, dict)
            self.assertEqual(len(result), 1)

    def test_remove_numbers_from_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = os.path.join(tmpdir, '001-test.txt')
            open(file1, 'w').close()
            
            result = remove_numbers_from_files([file1])
            self.assertIsInstance(result, dict)
            self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()