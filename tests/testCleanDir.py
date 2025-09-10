#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Unit tests for cleanDir module.
"""

import unittest
import tempfile
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from daptools.cleanDir import filter_files
from daptools.myTools import get_file_extension


class TestCleanDir(unittest.TestCase):

    def test_filter_files(self):
        test_files = ['test.aux', 'test.log', 'test.gz', 'test.tex', 'test.pdf']
        filtered = filter_files(test_files)
        self.assertIn('test.aux', filtered)
        self.assertIn('test.log', filtered)
        self.assertIn('test.gz', filtered)
        self.assertNotIn('test.tex', filtered)
        self.assertNotIn('test.pdf', filtered)

    def test_get_file_extension(self):
        name, ext = get_file_extension('test.aux')
        self.assertEqual(name, 'test')
        self.assertEqual(ext, 'aux')

    def test_empty_file_list(self):
        filtered = filter_files([])
        self.assertEqual(len(filtered), 0)


if __name__ == '__main__':
    unittest.main()