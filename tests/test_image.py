import pytest
import tempfile
from pathlib import Path
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from src.a_gis import purify_image

def save_blank_file(path):
    img = np.zeros([100,100,3],dtype=np.uint8)
    img.fill(255) # numpy array!
    im = Image.fromarray(img) #convert numpy array to image
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
           
        im = Image.open(path)
        print(im.info)
        assert im.info != {}

        im = purify_image(im)
        print(im.info)
        assert im.info == {}

