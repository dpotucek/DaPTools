#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Unit tests for myTools module.

@author: David Potucek
"""

import unittest
import tempfile
import os
import shutil
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from daptools.myTools import (
    contains, tree_walker, separate_full_path, strip_extension,
    strip_czech_chars, get_file_extension, convert_in_2_mm, convert_mm_2_in,
    read_data_file, num_usr_in, str_enum_usr_in, rename_files, prepare_counter
)


class TestMyTools(unittest.TestCase):

    def test_contains(self):
        data = "super velky PAKO jako prako pAko pako PAKO"
        self.assertEqual(contains(data, "pako"), 4)
        self.assertEqual(contains(data, "pako", True), 1)
        self.assertEqual(contains(data, "xyz"), 0)

    def test_tree_walker(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            open(os.path.join(tmpdir, "file1.txt"), 'w').close()
            subdir = os.path.join(tmpdir, "subdir")
            os.mkdir(subdir)
            open(os.path.join(subdir, "file2.txt"), 'w').close()
            
            files = tree_walker(tmpdir)
            self.assertEqual(len(files), 2)
            
            files_non_recursive = tree_walker(tmpdir, False)
            self.assertEqual(len(files_non_recursive), 1)

    def test_separate_full_path(self):
        path, filename = separate_full_path("/home/user/file.txt")
        self.assertEqual(path, "/home/user/")
        self.assertEqual(filename, "file.txt")

    def test_strip_extension(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp_path = tmp.name
        
        new_path = strip_extension(tmp_path, False)
        self.assertEqual(new_path, tmp_path[:-4])
        os.unlink(tmp_path)

    def test_strip_czech_chars(self):
        czech = "Příliš žluťoučký kůň"
        result = strip_czech_chars(czech)
        self.assertEqual(result, "Prilis zlutoucky kun")

    def test_get_file_extension(self):
        name, ext = get_file_extension("file.txt")
        self.assertEqual(name, "file")
        self.assertEqual(ext, "txt")
        
        name, ext = get_file_extension("noext")
        self.assertEqual(name, "")
        self.assertEqual(ext, "oext")

    def test_convert_in_2_mm(self):
        self.assertAlmostEqual(convert_in_2_mm(1), 25.4)
        self.assertAlmostEqual(convert_in_2_mm(2), 50.8)

    def test_convert_mm_2_in(self):
        self.assertAlmostEqual(convert_mm_2_in(25.4), 1)
        self.assertAlmostEqual(convert_mm_2_in(50.8), 2)

    def test_read_data_file(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write("; comment\n")
            tmp.write("STARTOFDATA\n")
            tmp.write("data line 1\n")
            tmp.write("data line 2\n")
            tmp.write("ENDOFDATA\n")
            tmp.write("ignored\n")
            tmp_path = tmp.name
        
        data = read_data_file(tmp_path)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0].strip(), "data line 1")
        os.unlink(tmp_path)

    def test_rename_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            old_file = os.path.join(tmpdir, "old.txt")
            new_file = os.path.join(tmpdir, "new.txt")
            open(old_file, 'w').close()
            
            rename_files({old_file: new_file})
            self.assertFalse(os.path.exists(old_file))
            self.assertTrue(os.path.exists(new_file))

    def test_prepare_counter(self):
        self.assertEqual(prepare_counter(5), "005")
        self.assertEqual(prepare_counter(42, 5), "00042")
        self.assertEqual(prepare_counter(123, 2), "123")


if __name__ == '__main__':
    unittest.main()