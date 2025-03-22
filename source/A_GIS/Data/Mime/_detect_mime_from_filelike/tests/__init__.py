"""Tests for _detect_mime_from_filelike function."""

import io
import pytest
import A_GIS.Data.Mime._detect_mime_from_filelike

def test_detect_mime_from_filelike_with_pdf():
    """Test detecting MIME type from a PDF file-like object."""
    pdf_content = b"%PDF-1.4\n%EOF"
    file_obj = io.BytesIO(pdf_content)
    result = A_GIS.Data.Mime._detect_mime_from_filelike._detect_mime_from_filelike(source=file_obj)
    assert result == "application/pdf"

def test_detect_mime_from_filelike_with_png():
    """Test detecting MIME type from a PNG file-like object."""
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
    file_obj = io.BytesIO(png_content)
    result = A_GIS.Data.Mime._detect_mime_from_filelike._detect_mime_from_filelike(source=file_obj)
    assert result == "image/png"

def test_detect_mime_from_filelike_with_seek():
    """Test that file position is preserved after reading."""
    content = b"test content"
    file_obj = io.BytesIO(content)
    initial_pos = file_obj.tell()
    
    A_GIS.Data.Mime._detect_mime_from_filelike._detect_mime_from_filelike(source=file_obj)
    
    assert file_obj.tell() == initial_pos

def test_detect_mime_from_filelike_without_seek():
    """Test with a file-like object without seek capability."""
    class NoSeekFile:
        def read(self, size):
            return b"test"
    
    file_obj = NoSeekFile()
    result = A_GIS.Data.Mime._detect_mime_from_filelike._detect_mime_from_filelike(source=file_obj)
    assert result is not None

def test_detect_mime_from_filelike_invalid_source():
    """Test that invalid source raises ValueError."""
    with pytest.raises(ValueError, match="Source must be a file-like object with a read method"):
        A_GIS.Data.Mime._detect_mime_from_filelike._detect_mime_from_filelike(source="not a file") 