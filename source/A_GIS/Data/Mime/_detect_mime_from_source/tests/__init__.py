"""
Tests for MIME type detection from file paths, URLs, and file-like objects.
"""

import unittest
import pathlib
import tempfile
import io
import os

import A_GIS.Data.Mime._detect_mime_from_source

class TestDetectMimeFromSource(unittest.TestCase):
    """Tests for MIME type detection from various source types."""
    
    def test_file_like_object(self):
        """Test detection from file-like object."""
        text_data = b'Hello, world!'
        file_obj = io.BytesIO(text_data)
        self.assertEqual(
            A_GIS.Data.Mime._detect_mime_from_source(source=file_obj),
            'text/plain'
        )
    
    def test_file_path(self):
        """Test detection from file path."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
            tmp.write(b'{"test": "data"}')
            tmp_path = tmp.name
        
        try:
            # Test with string path
            self.assertEqual(
                A_GIS.Data.Mime._detect_mime_from_source(source=tmp_path),
                'application/json'
            )
            
            # Test with Path object
            path_obj = pathlib.Path(tmp_path)
            self.assertEqual(
                A_GIS.Data.Mime._detect_mime_from_source(source=path_obj),
                'application/json'
            )
            
            # Test URL detection
            url = f"file://{tmp_path}"
            self.assertEqual(
                A_GIS.Data.Mime._detect_mime_from_source(source=url),
                'application/json'
            )
            
            # Test extension-only detection with a non-existent path
            fake_path = "/path/to/nonexistent/file.mp4"
            self.assertEqual(
                A_GIS.Data.Mime._detect_mime_from_source(source=fake_path),
                'video/mp4'
            )
        finally:
            os.unlink(tmp_path)

if __name__ == '__main__':
    unittest.main() 