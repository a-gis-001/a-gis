import os
import pytest
import A_GIS.File.Directory


def test_tempdir_creation():
    """Test if the TempDir creates a directory."""
    with A_GIS.File.Directory.make() as temp_dir:
        assert os.path.isdir(temp_dir.path), "Directory should be created"


def test_tempdir_custom_path():
    """Test TempDir with a custom path."""
    custom_path = "my_temp_dir"
    with A_GIS.File.Directory.make(path=custom_path) as temp_dir:
        assert (
            temp_dir.path == custom_path
        ), "Directory path should match the custom path"
        assert os.path.isdir(custom_path), "Custom directory should be created"
    # Clean up
    if os.path.exists(custom_path):
        os.rmdir(custom_path)


def test_tempdir_scoped_delete():
    """Test if the TempDir deletes itself when scoped_delete is True."""
    with A_GIS.File.Directory.make(scoped_delete=True) as temp_dir:
        path = temp_dir.path
    assert not os.path.exists(
        path
    ), "Directory should be deleted after exiting the context block"


def test_tempdir_no_delete():
    """Test if the TempDir does not delete itself when scoped_delete is False."""
    with A_GIS.File.Directory.make(scoped_delete=False) as temp_dir:
        path = temp_dir.path
    assert os.path.exists(
        path
    ), "Directory should not be deleted after exiting the context block"
    # Clean up
    os.rmdir(path)


def test_tempdir_destructor():
    """Test the destructor of TempDir for self-deletion."""
    temp_dir = A_GIS.File.Directory.make(scoped_delete=True)
    path = temp_dir.path
    del temp_dir
    assert not os.path.exists(
        path
    ), "Directory should be deleted when the object is destructed"
