import pytest
import A_GIS.Image


def test_remove_metadata():
    """Test that metadata is removed."""

    im1 = A_GIS.Image.new(size=(10, 10), metadata={"hello": "world"})
    assert A_GIS.Image.Metadata.get(image=im1) != {}

    im2 = A_GIS.Image.Metadata.remove(image=im1)
    assert A_GIS.Image.Metadata.get(image=im2) == {}
