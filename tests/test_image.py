import pytest
import tempfile
from pathlib import Path
import numpy as np
from PIL import Image as PImage
from PIL.PngImagePlugin import PngInfo
import a_gis

def save_blank_file(path):
    img = np.zeros([100,100,3],dtype=np.uint8)
    img.fill(255) # numpy array!
    im = PImage.fromarray(img) #convert numpy array to image
    metadata = PngInfo()
    metadata.add_text("MyNewString", "A string")
    metadata.add_text("MyNewInt", str(1234))
    im.save(path,pnginfo=metadata)

def test_remove_metadata():
    """ Test that metadata is removed by purify method. """

    with tempfile.TemporaryDirectory() as tmpdirname:
        print('created temporary directory', tmpdirname)
        path = Path(tmpdirname)/'blank.png'    
        save_blank_file(path)
           
        im0 = a_gis.Image.open(path=path)
        print(im0.info)
        assert im0.info != {}

        im1 = a_gis.image.purify(image=im0)
        print(im1.info)
        assert im1.info == {}

