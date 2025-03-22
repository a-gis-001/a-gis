"""
Tests for MIME detection functionality.

This module integrates all tests for the Mime detection functionality:
1. detect - The public API
2. _detect_mime_type - Internal function for binary data
3. _detect_mime_from_source - Internal function for various source types
"""

import unittest
import pathlib
import tempfile
import io
import os

import A_GIS.Data.Mime.detect

class TestDetect(unittest.TestCase):
    """Tests for the public detect function."""
    
    def test_detect_binary_data(self):
        """Test detection from binary data."""
        pdf_magic_bytes = b'%PDF-1.5'
        self.assertEqual(A_GIS.Data.Mime.detect(data_or_source=pdf_magic_bytes), 'application/pdf')
    
    def test_detect_file_like(self):
        """Test detection from file-like object."""
        text_data = b'Hello, world!'
        file_obj = io.BytesIO(text_data)
        self.assertEqual(A_GIS.Data.Mime.detect(data_or_source=file_obj), 'text/plain')
    
    def test_detect_file_path(self):
        """Test detection from file path."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
            tmp.write(b'{"test": "data"}')
            tmp_path = tmp.name
        
        try:
            self.assertEqual(A_GIS.Data.Mime.detect(data_or_source=tmp_path), 'application/json')
        finally:
            os.unlink(tmp_path)

if __name__ == '__main__':
    unittest.main() 