#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Unit tests for sphericalGeodesy module.
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from daptools.sphericalGeodesy import haversine_distance, calculate_bearing, destination_point


class TestSphericalGeodesy(unittest.TestCase):

    def test_haversine_distance(self):
        # Distance between Prague and Vienna (approximately 250 km)
        prague = (50.0755, 14.4378)
        vienna = (48.2082, 16.3738)
        
        distance = haversine_distance(prague[0], prague[1], vienna[0], vienna[1])
        self.assertAlmostEqual(distance, 250, delta=10)  # Within 10 km tolerance

    def test_calculate_bearing(self):
        # Bearing from Prague to Vienna (approximately southeast)
        prague = (50.0755, 14.4378)
        vienna = (48.2082, 16.3738)
        
        bearing = calculate_bearing(prague[0], prague[1], vienna[0], vienna[1])
        self.assertGreater(bearing, 90)  # Southeast quadrant
        self.assertLess(bearing, 180)

    def test_destination_point(self):
        # Starting from Prague, go 100km north
        prague = (50.0755, 14.4378)
        
        dest_lat, dest_lon = destination_point(prague[0], prague[1], 0, 100)  # 0° = north
        self.assertGreater(dest_lat, prague[0])  # Should be further north
        self.assertAlmostEqual(dest_lon, prague[1], delta=0.1)  # Longitude should be similar


if __name__ == '__main__':
    unittest.main()