#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Unit tests for unitsBatch module.
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from daptools.unitsBatch import parse_fraction, parse_number, check_fraction_validity


class TestUnitsBatch(unittest.TestCase):

    def test_parse_fraction(self):
        self.assertAlmostEqual(parse_fraction("1/2"), 0.5)
        self.assertAlmostEqual(parse_fraction("3/4"), 0.75)
        self.assertAlmostEqual(parse_fraction("2/8"), 0.25)

    def test_parse_number(self):
        self.assertAlmostEqual(parse_number("1/2"), 0.5)
        self.assertAlmostEqual(parse_number("2.5"), 2.5)
        self.assertAlmostEqual(parse_number("10"), 10.0)

    def test_check_fraction_validity(self):
        self.assertTrue(check_fraction_validity("1/2"))
        self.assertTrue(check_fraction_validity("3/4"))
        self.assertFalse(check_fraction_validity("1/2/3"))  # Double slash invalid


if __name__ == '__main__':
    unittest.main()