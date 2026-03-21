#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Unit tests for standardAtmosphere module.
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from daptools.standardAtmosphere import (
    get_atmosphere_properties, altitude_to_pressure, pressure_to_altitude,
    density_altitude, simple_atm, STANDARD_PRESSURE, STANDARD_TEMPERATURE, STANDARD_DENSITY
)


class TestStandardAtmosphere(unittest.TestCase):

    def test_sea_level_properties(self):
        """Test standard atmosphere at sea level."""
        props = get_atmosphere_properties(0)
        self.assertAlmostEqual(props['pressure'], STANDARD_PRESSURE, delta=1)
        self.assertAlmostEqual(props['temperature'], STANDARD_TEMPERATURE, delta=0.01)
        self.assertAlmostEqual(props['density'], STANDARD_DENSITY, delta=0.001)
        self.assertAlmostEqual(props['sound_speed'], 340.294, delta=0.1)

    def test_troposphere_properties(self):
        """Test properties in troposphere (0-11km)."""
        props = get_atmosphere_properties(5000)
        # Temperature decreases with altitude
        self.assertLess(props['temperature'], STANDARD_TEMPERATURE)
        # Pressure decreases with altitude
        self.assertLess(props['pressure'], STANDARD_PRESSURE)
        # Density decreases with altitude
        self.assertLess(props['density'], STANDARD_DENSITY)
        # All values positive
        self.assertGreater(props['temperature'], 0)
        self.assertGreater(props['pressure'], 0)
        self.assertGreater(props['density'], 0)

    def test_tropopause_properties(self):
        """Test properties at tropopause (11km)."""
        props = get_atmosphere_properties(11000)
        # Temperature at tropopause is approximately 216.65 K
        self.assertAlmostEqual(props['temperature'], 216.65, delta=1)
        # Pressure approximately 22632 Pa
        self.assertAlmostEqual(props['pressure'], 22632, delta=500)

    def test_stratosphere_properties(self):
        """Test properties in stratosphere (11-47km)."""
        props = get_atmosphere_properties(25000)
        # Temperature in stratosphere
        self.assertGreater(props['temperature'], 200)
        self.assertLess(props['temperature'], 230)
        # Pressure continues to decrease
        self.assertLess(props['pressure'], 22632)

    def test_altitude_to_pressure(self):
        """Test altitude to pressure conversion."""
        # Sea level
        pressure = altitude_to_pressure(0)
        self.assertAlmostEqual(pressure, STANDARD_PRESSURE, delta=1)
        
        # 5000m
        pressure_5km = altitude_to_pressure(5000)
        self.assertLess(pressure_5km, STANDARD_PRESSURE)
        self.assertGreater(pressure_5km, 50000)
        
        # Pressure decreases with altitude
        pressure_10km = altitude_to_pressure(10000)
        self.assertLess(pressure_10km, pressure_5km)

    def test_pressure_to_altitude(self):
        """Test pressure to altitude conversion."""
        # Standard sea level pressure
        altitude = pressure_to_altitude(STANDARD_PRESSURE)
        self.assertAlmostEqual(altitude, 0, delta=10)
        
        # Lower pressure gives higher altitude
        altitude_high = pressure_to_altitude(50000)
        self.assertGreater(altitude_high, 5000)
        self.assertLess(altitude_high, 6000)

    def test_pressure_altitude_roundtrip(self):
        """Test roundtrip conversion altitude->pressure->altitude."""
        test_altitudes = [0, 1000, 5000, 10000, 20000]
        for alt in test_altitudes:
            pressure = altitude_to_pressure(alt)
            alt_back = pressure_to_altitude(pressure)
            self.assertAlmostEqual(alt, alt_back, delta=1)

    def test_density_altitude_standard_conditions(self):
        """Test density altitude under standard conditions."""
        # At standard temperature, density altitude equals pressure altitude
        da = density_altitude(1000, 15 - 0.0065 * 1000, 0)
        self.assertAlmostEqual(da, 1000, delta=50)

    def test_density_altitude_hot_conditions(self):
        """Test density altitude in hot conditions."""
        # Hot temperature increases density altitude
        da = density_altitude(1000, 30, 0)
        self.assertGreater(da, 1000)

    def test_density_altitude_cold_conditions(self):
        """Test density altitude in cold conditions."""
        # Cold temperature decreases density altitude
        da = density_altitude(1000, 0, 0)
        self.assertLess(da, 1000)

    def test_density_altitude_with_humidity(self):
        """Test density altitude with humidity effects."""
        # Humidity increases density altitude (reduces density)
        da_dry = density_altitude(1000, 25, 0)
        da_humid = density_altitude(1000, 25, 80)
        self.assertGreater(da_humid, da_dry)

    def test_simple_atm_sea_level(self):
        """Test simple_atm function at sea level."""
        hust, tlk, tplt, spd = simple_atm(0)
        self.assertAlmostEqual(tlk, 1013.25, delta=0.1)
        self.assertAlmostEqual(tplt, 15, delta=0.1)
        self.assertAlmostEqual(hust, 1.225, delta=0.01)

    def test_simple_atm_altitude(self):
        """Test simple_atm function at altitude."""
        hust, tlk, tplt, spd = simple_atm(5000)
        # Values decrease with altitude
        self.assertLess(tlk, 1013.25)
        self.assertLess(tplt, 15)
        self.assertLess(hust, 1.225)

    def test_simple_atm_limit(self):
        """Test simple_atm raises error above 11km."""
        with self.assertRaises(ValueError):
            simple_atm(12000)

    def test_invalid_altitude_negative(self):
        """Test error handling for negative altitude."""
        with self.assertRaises(ValueError):
            get_atmosphere_properties(-100)

    def test_invalid_altitude_too_high(self):
        """Test error handling for altitude above 84852m."""
        with self.assertRaises(ValueError):
            get_atmosphere_properties(90000)

    def test_viscosity_properties(self):
        """Test viscosity calculations."""
        props = get_atmosphere_properties(0)
        self.assertGreater(props['viscosity'], 0)
        self.assertGreater(props['kinematic_viscosity'], 0)
        # Kinematic viscosity = viscosity / density
        expected_nu = props['viscosity'] / props['density']
        self.assertAlmostEqual(props['kinematic_viscosity'], expected_nu, delta=1e-9)


if __name__ == '__main__':
    unittest.main()