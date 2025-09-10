#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Unit tests for mathPhys module.
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from daptools.mathPhys import deg2rad, rad2deg, c2f, f2c, fibonacci, degree2decimal, decimal2degree


class TestMathPhys(unittest.TestCase):

    def test_deg2rad(self):
        self.assertAlmostEqual(deg2rad(0), 0)
        self.assertAlmostEqual(deg2rad(90), 1.5707963267948966)
        self.assertAlmostEqual(deg2rad(180), 3.141592653589793)

    def test_rad2deg(self):
        self.assertAlmostEqual(rad2deg(0), 0)
        self.assertAlmostEqual(rad2deg(1.5707963267948966), 90)
        self.assertAlmostEqual(rad2deg(3.141592653589793), 180)

    def test_c2f(self):
        self.assertAlmostEqual(c2f(0), 32)
        self.assertAlmostEqual(c2f(100), 212)
        self.assertAlmostEqual(c2f(-40), -40)

    def test_f2c(self):
        self.assertAlmostEqual(f2c(32), 0)
        self.assertAlmostEqual(f2c(212), 100)
        self.assertAlmostEqual(f2c(-40), -40)

    def test_fibonacci(self):
        fib_list = list(fibonacci(5))
        self.assertEqual(len(fib_list), 6)  # Function returns 6 numbers for input 5
        self.assertEqual(fib_list[0], 0)
        self.assertEqual(fib_list[1], 1)
        self.assertEqual(fib_list[2], 1)

    def test_degree2decimal(self):
        result = degree2decimal(50, 19, 9.652, 'N')
        self.assertAlmostEqual(result, 50.319348, places=5)

    def test_decimal2degree(self):
        d, m, s = decimal2degree(50.319348)
        self.assertEqual(d, 50)
        self.assertEqual(m, 19)
        self.assertAlmostEqual(s, 9.652, places=2)


if __name__ == '__main__':
    unittest.main()