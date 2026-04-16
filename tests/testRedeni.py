#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Unit tests for redeni module (solution dilution and mixing).
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from daptools.redeni import dilution, mixing


class TestDilution(unittest.TestCase):
    """Tests for dilution function."""
    
    def test_dilution_basic(self):
        """Test basic dilution calculation."""
        # 1 liter of 74% alcohol diluted to 40%
        v_voda = dilution(1.0, 74.0, 40.0)
        self.assertAlmostEqual(v_voda, 0.85, places=2)
    
    def test_dilution_small_volume(self):
        """Test dilution with small volume."""
        # 0.5 liter of 96% alcohol diluted to 40%
        v_voda = dilution(0.5, 96.0, 40.0)
        self.assertAlmostEqual(v_voda, 0.7, places=1)
    
    def test_dilution_large_volume(self):
        """Test dilution with large volume."""
        # 10 liters of 80% alcohol diluted to 50%
        v_voda = dilution(10.0, 80.0, 50.0)
        self.assertAlmostEqual(v_voda, 6.0, places=1)
    
    def test_dilution_small_difference(self):
        """Test dilution with small concentration difference."""
        # 1 liter of 50% alcohol diluted to 45%
        v_voda = dilution(1.0, 50.0, 45.0)
        self.assertAlmostEqual(v_voda, 0.111, places=2)
    
    def test_dilution_invalid_negative_volume(self):
        """Test error handling for negative volume."""
        with self.assertRaises(ValueError) as context:
            dilution(-1.0, 74.0, 40.0)
        self.assertIn("kladné číslo", str(context.exception))
    
    def test_dilution_invalid_zero_volume(self):
        """Test error handling for zero volume."""
        with self.assertRaises(ValueError):
            dilution(0.0, 74.0, 40.0)
    
    def test_dilution_invalid_concentration_too_high(self):
        """Test error handling for concentration > 100%."""
        with self.assertRaises(ValueError) as context:
            dilution(1.0, 150.0, 40.0)
        self.assertIn("mezi 0 a 100", str(context.exception))
    
    def test_dilution_invalid_concentration_negative(self):
        """Test error handling for negative concentration."""
        with self.assertRaises(ValueError):
            dilution(1.0, -10.0, 40.0)
    
    def test_dilution_invalid_target_higher(self):
        """Test error handling when target concentration is higher than initial."""
        with self.assertRaises(ValueError) as context:
            dilution(1.0, 40.0, 74.0)
        self.assertIn("nižší než počáteční", str(context.exception))
    
    def test_dilution_invalid_target_equal(self):
        """Test error handling when target equals initial concentration."""
        with self.assertRaises(ValueError):
            dilution(1.0, 50.0, 50.0)


class TestMixing(unittest.TestCase):
    """Tests for mixing function."""
    
    def test_mixing_basic(self):
        """Test basic mixing calculation."""
        # 10 liters of 40% from 74% alcohol
        v_alkohol, v_voda = mixing(10.0, 74.0, 40.0)
        self.assertAlmostEqual(v_alkohol, 5.405, places=2)
        self.assertAlmostEqual(v_voda, 4.595, places=2)
        self.assertAlmostEqual(v_alkohol + v_voda, 10.0, places=2)
    
    def test_mixing_small_volume(self):
        """Test mixing with small target volume."""
        # 0.5 liters of 40% from 96% alcohol
        v_alkohol, v_voda = mixing(0.5, 96.0, 40.0)
        self.assertAlmostEqual(v_alkohol, 0.208, places=2)
        self.assertAlmostEqual(v_voda, 0.292, places=2)
    
    def test_mixing_large_volume(self):
        """Test mixing with large target volume."""
        # 100 liters of 50% from 80% alcohol
        v_alkohol, v_voda = mixing(100.0, 80.0, 50.0)
        self.assertAlmostEqual(v_alkohol, 62.5, places=1)
        self.assertAlmostEqual(v_voda, 37.5, places=1)
    
    def test_mixing_high_concentration(self):
        """Test mixing with high target concentration."""
        # 1 liter of 90% from 96% alcohol
        v_alkohol, v_voda = mixing(1.0, 96.0, 90.0)
        self.assertAlmostEqual(v_alkohol, 0.9375, places=3)
        self.assertAlmostEqual(v_voda, 0.0625, places=3)
    
    def test_mixing_low_concentration(self):
        """Test mixing with low target concentration."""
        # 1 liter of 10% from 50% alcohol
        v_alkohol, v_voda = mixing(1.0, 50.0, 10.0)
        self.assertAlmostEqual(v_alkohol, 0.2, places=2)
        self.assertAlmostEqual(v_voda, 0.8, places=2)
    
    def test_mixing_same_concentration(self):
        """Test mixing when target equals initial concentration."""
        # 1 liter of 50% from 50% alcohol (no water needed)
        v_alkohol, v_voda = mixing(1.0, 50.0, 50.0)
        self.assertAlmostEqual(v_alkohol, 1.0, places=2)
        self.assertAlmostEqual(v_voda, 0.0, places=2)
    
    def test_mixing_volume_sum(self):
        """Test that alcohol + water equals target volume."""
        v_alkohol, v_voda = mixing(5.0, 70.0, 35.0)
        self.assertAlmostEqual(v_alkohol + v_voda, 5.0, places=6)
    
    def test_mixing_invalid_negative_volume(self):
        """Test error handling for negative target volume."""
        with self.assertRaises(ValueError) as context:
            mixing(-1.0, 74.0, 40.0)
        self.assertIn("kladné číslo", str(context.exception))
    
    def test_mixing_invalid_zero_volume(self):
        """Test error handling for zero target volume."""
        with self.assertRaises(ValueError):
            mixing(0.0, 74.0, 40.0)
    
    def test_mixing_invalid_concentration_too_high(self):
        """Test error handling for concentration > 100%."""
        with self.assertRaises(ValueError) as context:
            mixing(1.0, 150.0, 40.0)
        self.assertIn("mezi 0 a 100", str(context.exception))
    
    def test_mixing_invalid_concentration_negative(self):
        """Test error handling for negative concentration."""
        with self.assertRaises(ValueError):
            mixing(1.0, -10.0, 40.0)
    
    def test_mixing_invalid_target_higher(self):
        """Test error handling when target concentration is higher than available."""
        with self.assertRaises(ValueError) as context:
            mixing(1.0, 40.0, 74.0)
        self.assertIn("nemůže být vyšší", str(context.exception))


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""
    
    def test_dilution_very_small_concentration_difference(self):
        """Test dilution with very small concentration difference."""
        v_voda = dilution(1.0, 50.0, 49.9)
        self.assertGreater(v_voda, 0)
        self.assertLess(v_voda, 0.01)
    
    def test_mixing_very_small_target_concentration(self):
        """Test mixing with very small target concentration."""
        v_alkohol, v_voda = mixing(1.0, 96.0, 1.0)
        self.assertAlmostEqual(v_alkohol, 0.0104, places=3)
        self.assertAlmostEqual(v_voda, 0.9896, places=3)
    
    def test_dilution_precision(self):
        """Test dilution calculation precision."""
        # Verify the formula: v_voda = v_start * (c_poc / c_cil - 1)
        v_start = 2.5
        c_poc = 80.0
        c_cil = 45.0
        v_voda = dilution(v_start, c_poc, c_cil)
        expected = v_start * (c_poc / c_cil - 1)
        self.assertAlmostEqual(v_voda, expected, places=10)
    
    def test_mixing_precision(self):
        """Test mixing calculation precision."""
        # Verify the formula: v_alkohol = v_cil * (c_cil / c_poc)
        v_cil = 3.7
        c_poc = 85.0
        c_cil = 42.0
        v_alkohol, v_voda = mixing(v_cil, c_poc, c_cil)
        expected_alkohol = v_cil * (c_cil / c_poc)
        expected_voda = v_cil - expected_alkohol
        self.assertAlmostEqual(v_alkohol, expected_alkohol, places=10)
        self.assertAlmostEqual(v_voda, expected_voda, places=10)


if __name__ == '__main__':
    unittest.main()
