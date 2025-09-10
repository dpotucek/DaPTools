#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Unit tests for logger module.
"""

import unittest
import tempfile
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from daptools.logger import DataLoger


class TestLogger(unittest.TestCase):

    def test_data_loger_creation(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name
        
        logger = DataLoger(tmp_path)
        self.assertIsInstance(logger, DataLoger)
        self.assertEqual(logger.soubor, tmp_path)
        os.unlink(tmp_path)

    def test_write_event(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp_path = tmp.name
        
        logger = DataLoger(tmp_path)
        logger.write_event('Test event')
        
        with open(tmp_path, 'r', encoding='utf8') as f:
            content = f.read()
        
        self.assertIn('Test event', content)
        os.unlink(tmp_path)

    def test_multiple_events(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp_path = tmp.name
        
        logger = DataLoger(tmp_path)
        logger.write_event('Event 1')
        logger.write_event('Event 2')
        
        with open(tmp_path, 'r', encoding='utf8') as f:
            content = f.read()
        
        self.assertIn('Event 1', content)
        self.assertIn('Event 2', content)
        os.unlink(tmp_path)


if __name__ == '__main__':
    unittest.main()