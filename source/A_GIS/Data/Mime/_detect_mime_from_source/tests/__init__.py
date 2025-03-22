"""
Tests for MIME type detection from file paths, URLs, and file-like objects.
"""

import unittest
import pathlib
import tempfile
import io
import os
import pytest

import A_GIS.Data.Mime._detect_mime_from_source

class TestDetectMimeFromSource(unittest.TestCase):
    """Test cases for _detect_mime_from_source function."""
    
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
            
            # Test with pathlib.Path
            self.assertEqual(
                A_GIS.Data.Mime._detect_mime_from_source(source=pathlib.Path(tmp_path)),
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
            with pytest.raises(ValueError, match="Path does not point to a file"):
                A_GIS.Data.Mime._detect_mime_from_source(source=fake_path)
        finally:
            os.unlink(tmp_path)

def test_detect_mime_from_source_filelike():
    """Test detecting MIME type from file-like object."""
    pdf_content = b"%PDF-1.4\n%EOF"
    file_obj = io.BytesIO(pdf_content)
    result = A_GIS.Data.Mime._detect_mime_from_source(source=file_obj)
    assert result == "application/pdf"

def test_detect_mime_from_source_url():
    """Test detecting MIME type from URL."""
    url = "http://example.com/file.pdf"
    result = A_GIS.Data.Mime._detect_mime_from_source(source=url)
    assert result == "application/pdf"

def test_detect_mime_from_source_path():
    """Test detecting MIME type from file path."""
    # Include IHDR chunk for a more complete PNG file
    png_content = (
        b"\x89PNG\r\n\x1a\n"  # PNG signature
        b"\x00\x00\x00\x0D"   # IHDR chunk length
        b"IHDR"               # IHDR chunk type
        b"\x00\x00\x00\x01"   # Width: 1 pixel
        b"\x00\x00\x00\x01"   # Height: 1 pixel
        b"\x08"               # Bit depth: 8
        b"\x06"               # Color type: RGBA
        b"\x00"               # Compression: standard
        b"\x00"               # Filter: standard
        b"\x00"               # Interlace: none
        b"\x1f\x15\xc4\x89"   # CRC
        b"\x00\x00\x00\x00"   # IEND chunk length
        b"IEND"               # IEND chunk type
        b"\xae\x42\x60\x82"   # IEND CRC
    )
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(png_content)
        tmp_path = tmp.name
    
    try:
        result = A_GIS.Data.Mime._detect_mime_from_source(source=tmp_path)
        assert result == "image/png"
    finally:
        os.unlink(tmp_path)

def test_detect_mime_from_source_pathlib():
    """Test detecting MIME type from pathlib.Path object."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp.write(b"{}")
        tmp_path = pathlib.Path(tmp.name)
    
    try:
        result = A_GIS.Data.Mime._detect_mime_from_source(source=tmp_path)
        assert result == "application/json"
    finally:
        os.unlink(tmp_path)

def test_detect_mime_from_source_custom_sniff_bytes():
    """Test with custom sniff_bytes parameter."""
    pdf_content = b"%PDF-1.4\n%EOF"
    file_obj = io.BytesIO(pdf_content)
    result = A_GIS.Data.Mime._detect_mime_from_source(
        source=file_obj, sniff_bytes=1024
    )
    assert result == "application/pdf"

def test_detect_mime_from_source_nonexistent_file():
    """Test with nonexistent file path."""
    with pytest.raises(ValueError, match="Path does not point to a file"):
        A_GIS.Data.Mime._detect_mime_from_source(source="/nonexistent/file.txt")

if __name__ == '__main__':
    unittest.main() 