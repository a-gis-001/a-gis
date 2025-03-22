"""Tests for _detect_mime_from_url function."""

import pytest

import A_GIS.Data.Mime._detect_mime_from_url

def test_detect_mime_from_url_http():
    """Test detecting MIME type from HTTP URL."""
    url = "http://example.com/file.pdf"
    result = A_GIS.Data.Mime._detect_mime_from_url._detect_mime_from_url(url=url)
    assert result == "application/pdf"

def test_detect_mime_from_url_https():
    """Test detecting MIME type from HTTPS URL."""
    url = "https://example.com/image.png"
    result = A_GIS.Data.Mime._detect_mime_from_url._detect_mime_from_url(url=url)
    assert result == "image/png"

def test_detect_mime_from_url_ftp():
    """Test detecting MIME type from FTP URL."""
    url = "ftp://example.com/document.doc"
    result = A_GIS.Data.Mime._detect_mime_from_url._detect_mime_from_url(url=url)
    assert result == "application/msword"

def test_detect_mime_from_url_file():
    """Test detecting MIME type from file URL."""
    url = "file:///path/to/file.jpg"
    result = A_GIS.Data.Mime._detect_mime_from_url._detect_mime_from_url(url=url)
    assert result == "image/jpeg"

def test_detect_mime_from_url_invalid_protocol():
    """Test that invalid protocol raises ValueError."""
    url = "invalid://example.com/file.txt"
    with pytest.raises(ValueError, match="URL must use http, https, ftp, or file protocol"):
        A_GIS.Data.Mime._detect_mime_from_url._detect_mime_from_url(url=url)

def test_detect_mime_from_url_no_extension():
    """Test URL with no file extension."""
    url = "http://example.com/file"
    result = A_GIS.Data.Mime._detect_mime_from_url._detect_mime_from_url(url=url)
    assert result is None 