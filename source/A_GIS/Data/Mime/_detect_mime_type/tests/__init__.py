def test_detect_mime_type():
    """
    Tests for MIME type detection from binary data.
    """
    import A_GIS.Data.Mime._detect_mime_type
    
    # Test binary data detection
    pdf_magic_bytes = b'%PDF-1.5'
    assert A_GIS.Data.Mime._detect_mime_type._detect_mime_type(data=pdf_magic_bytes) == 'application/pdf'
    
    # Test empty data handling
    empty_data = b''
    mime = A_GIS.Data.Mime._detect_mime_type._detect_mime_type(data=empty_data)
    assert mime is None or isinstance(mime, str) 