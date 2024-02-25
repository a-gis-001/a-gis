import pytest
import tempfile
import pathlib
import A_GIS.Image

def requirements_RemovesMetadata():
    """ Test that metadata is removed. """

    with tempfile.TemporaryDirectory() as tmpdirname:
        print('created temporary directory', tmpdirname)
        path = pathlib.Path(tmpdirname)/'blank.png'

        im1 = A_GIS.Image.new(path=path,size=(10,10),metadata='{"hello":"world"}')
        assert A_GIS.Image.Metadata.get(image=im1) != {}

        im2 = A_GIS.Image.Metadata.remove(image=im2)
        assert A_GIS.Image.Metadata.get(image=im2) == {}

