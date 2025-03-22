"""
Tests for MIME type detection from binary data.
"""

import unittest
import A_GIS.Data.Mime._detect_mime_type

class TestDetectMimeType(unittest.TestCase):
    """Tests for MIME type detection from binary data."""
    
    def test_detect_binary_data(self):
        """Test detection from binary data."""
        pdf_magic_bytes = b'%PDF-1.5'
        self.assertEqual(
            A_GIS.Data.Mime._detect_mime_type(data=pdf_magic_bytes),
            'application/pdf'
        )
    
    def test_empty_data(self):
        """Test handling of empty data."""
        empty_data = b''
        mime = A_GIS.Data.Mime._detect_mime_type(data=empty_data)
        self.assertIsNone(mime)

if __name__ == '__main__':
    unittest.main() 