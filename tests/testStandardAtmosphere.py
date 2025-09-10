#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Unit tests for standardAtmosphere module.
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from daptools.standardAtmosphere import get_atmosphere_properties, altitude_to_pressure, pressure_to_altitude


class TestStandardAtmosphere(unittest.TestCase):

    def test_get_atmosphere_properties(self):
        # Sea level properties
        props = get_atmosphere_properties(0)
        self.assertAlmostEqual(props['pressure'], 101325, delta=100)  # Pa
        self.assertAlmostEqual(props['temperature'], 288.15, delta=1)  # K
        self.assertAlmostEqual(props['density'], 1.225, delta=0.01)  # kg/m³

    def test_altitude_to_pressure(self):
        # Sea level pressure
        pressure = altitude_to_pressure(0)
        self.assertAlmostEqual(pressure, 101325, delta=100)
        
        # Pressure decreases with altitude
        pressure_high = altitude_to_pressure(10000)  # 10 km
        self.assertLess(pressure_high, pressure)

    def test_pressure_to_altitude(self):
        # Standard sea level pressure should give 0 altitude
        altitude = pressure_to_altitude(101325)
        self.assertAlmostEqual(altitude, 0, delta=10)
        
        # Lower pressure should give higher altitude
        altitude_high = pressure_to_altitude(50000)  # Lower pressure
        self.assertGreater(altitude_high, 0)


if __name__ == '__main__':
    unittest.main()