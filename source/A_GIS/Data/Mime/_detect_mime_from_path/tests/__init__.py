"""Tests for _detect_mime_from_path function."""

import os
import pytest
import tempfile
import pathlib
import A_GIS.Data.Mime._detect_mime_from_path

def test_detect_mime_from_path_with_pdf():
    """Test detecting MIME type from PDF file path."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(b"%PDF-1.4\n%EOF")
        tmp_path = tmp.name
    
    try:
        result = A_GIS.Data.Mime._detect_mime_from_path._detect_mime_from_path(path=tmp_path)
        assert result == "application/pdf"
    finally:
        os.unlink(tmp_path)

def test_detect_mime_from_path_with_png():
    """Test detecting MIME type from PNG file path."""
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
        result = A_GIS.Data.Mime._detect_mime_from_path._detect_mime_from_path(path=tmp_path)
        assert result == "image/png"
    finally:
        os.unlink(tmp_path)

def test_detect_mime_from_path_nonexistent():
    """Test that nonexistent file raises ValueError."""
    with pytest.raises(ValueError, match="Path does not point to a file"):
        A_GIS.Data.Mime._detect_mime_from_path._detect_mime_from_path(path="/nonexistent/file.txt")

def test_detect_mime_from_path_without_magic():
    """Test fallback to extension-based detection when magic is not available."""
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        tmp.write(b"plain text")
        tmp_path = tmp.name
    
    try:
        result = A_GIS.Data.Mime._detect_mime_from_path._detect_mime_from_path(path=tmp_path)
        assert result == "text/plain"
    finally:
        os.unlink(tmp_path)

def test_detect_mime_from_path_with_pathlib():
    """Test that function works with pathlib.Path objects."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp.write(b"{}")
        tmp_path = pathlib.Path(tmp.name)
    
    try:
        result = A_GIS.Data.Mime._detect_mime_from_path._detect_mime_from_path(path=str(tmp_path))
        assert result == "application/json"
    finally:
        os.unlink(tmp_path) 