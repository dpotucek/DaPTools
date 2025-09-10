#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Unit tests for MRIDValidator module.
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from daptools.MRIDValidator import validate_mrid, format_mrid


class TestMRIDValidator(unittest.TestCase):

    def test_validate_mrid(self):
        # Test valid MRID format
        valid_mrid = "12345678-1234-1234-1234-123456789012"
        self.assertTrue(validate_mrid(valid_mrid))
        
        # Test invalid MRID format
        invalid_mrid = "invalid-mrid"
        self.assertFalse(validate_mrid(invalid_mrid))

    def test_format_mrid(self):
        unformatted = "123456781234123412341234567890123456"
        formatted = format_mrid(unformatted)
        self.assertEqual(len(formatted.split('-')), 5)
        self.assertTrue(validate_mrid(formatted))


if __name__ == '__main__':
    unittest.main()