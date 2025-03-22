"""
Tests for MIME detection functionality.

This module integrates all tests for the Mime detection functionality:
1. detect - The public API
2. _detect_mime_type - Internal function for binary data
3. _detect_mime_from_source - Internal function for various source types
"""

def test_detect():
    """
    Tests for the public detect function.
    """
    import pathlib
    import tempfile
    import io
    import os
    
    import A_GIS.Data.Mime.detect
    
    # Test with binary data
    pdf_magic_bytes = b'%PDF-1.5'
    assert A_GIS.Data.Mime.detect.detect(data_or_source=pdf_magic_bytes) == 'application/pdf'
    
    # Test with file-like object
    text_data = b'Hello, world!'
    file_obj = io.BytesIO(text_data)
    assert A_GIS.Data.Mime.detect.detect(data_or_source=file_obj) == 'text/plain'
    
    # Test with file path
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
        tmp.write(b'{"test": "data"}')
        tmp_path = tmp.name
    
    try:
        assert A_GIS.Data.Mime.detect.detect(data_or_source=tmp_path) == 'application/json'
    finally:
        os.unlink(tmp_path) 