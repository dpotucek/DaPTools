#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Unit tests for generateSHA module.
"""

import unittest
import tempfile
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from daptools.generateSHA import get_hashsums, create_hash, validate_file


class TestGenerateSHA(unittest.TestCase):

    def test_get_hashsums(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write('test content')
            tmp_path = tmp.name
        
        hashes = get_hashsums(tmp_path)
        self.assertIn('sha256sum', hashes)
        self.assertIn('md5sum', hashes)
        self.assertEqual(len(hashes['sha256sum']), 64)
        self.assertEqual(len(hashes['md5sum']), 32)
        os.unlink(tmp_path)

    def test_create_hash(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write('test content')
            tmp_path = tmp.name
        
        hash_obj, hash_type = create_hash(tmp_path, 'sha256sum')
        self.assertEqual(hash_type, 'sha256sum')
        self.assertEqual(len(hash_obj.hexdigest()), 64)
        os.unlink(tmp_path)

    def test_validate_file(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write('test content')
            tmp_path = tmp.name
        
        hash_obj, _ = create_hash(tmp_path)
        correct_hash = hash_obj.hexdigest()
        
        result, _, _ = validate_file(tmp_path, correct_hash)
        self.assertTrue(result)
        
        result, _, _ = validate_file(tmp_path, 'wrong_hash')
        self.assertFalse(result)
        os.unlink(tmp_path)


if __name__ == '__main__':
    unittest.main()