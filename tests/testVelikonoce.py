#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Unit tests for velikonoce module.
"""

import unittest
import datetime
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from daptools.velikonoce import velikonoce


class TestVelikonoce(unittest.TestCase):

    def test_velikonoce_calculation(self):
        vel = velikonoce()
        
        # Test known Easter dates
        easter_2024 = vel.get_velikonoce(2024)
        self.assertEqual(easter_2024, (2024, 3, 31))
        
        easter_2008 = vel.get_velikonoce(2008)
        self.assertEqual(easter_2008, (2008, 3, 23))

    def test_coefficients(self):
        vel = velikonoce()
        d, e, rok = vel.coefficients(2008)
        self.assertEqual(d, 1)
        self.assertEqual(e, 0)
        self.assertEqual(rok, 2008)

    def test_validate_brezen(self):
        vel = velikonoce()
        self.assertTrue(vel.validate_brezen(23))
        self.assertFalse(vel.validate_brezen(32))
        self.assertFalse(vel.validate_brezen(0))

    def test_get_day_month(self):
        vel = velikonoce()
        result = vel.get_day_month((1, 0, 2008))
        self.assertEqual(result, (2008, 3, 23))


if __name__ == '__main__':
    unittest.main()