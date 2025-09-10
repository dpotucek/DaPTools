#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Unit tests for LaTeXHelper module.
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from daptools.LaTeXHelper import generate_table_row


class TestLaTeXHelper(unittest.TestCase):

    def test_generate_table_row(self):
        row = generate_table_row('first', 'second', 'third')
        self.assertIn('first & second & third', row)
        self.assertIn('\\\\', row)  # LaTeX line break

    def test_generate_table_row_single_arg(self):
        row = generate_table_row('single')
        self.assertEqual(row, 'single \\\\')

    def test_generate_table_row_numbers(self):
        row = generate_table_row(1, 2, 3)
        self.assertIn('1 & 2 & 3', row)
        self.assertIn('\\\\', row)

    def test_generate_table_row_mixed_types(self):
        row = generate_table_row('text', 42, 3.14)
        self.assertIn('text & 42 & 3.14', row)
        self.assertIn('\\\\', row)


if __name__ == '__main__':
    unittest.main()