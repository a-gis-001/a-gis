# Create a base class.
class Image():
    """The AEGIS Image class provides Use this image class in all client code."""
    def __init__(self,pil=None):
    
        # Initialize.
        self.content = None
        self.info = None
        self.mode = ''
        self.size = 0

        # Adapter to PIL input image.
        if pil:
            self.content = pil
            self.getdata = pil.getdata
            self.putdata = pil.putdata
            self.getpalette = pil.getpalette
            self.putpalette = pil.putpalette
            self.info = pil.info
            self.mode = pil.mode
            self.size = pil.size

    def getdata(self):
        return self.getdata()

    def putdata(self,data):
        return self.putdata(data)

    def getpalette(self):
        return self.getpalette()

    def putpalette(self,data):
        return self.putpalette(data)

    @staticmethod
    def open(*,path,**kwargs):
        from PIL import Image as PImage
        return Image( pil=PImage.open(path,**kwargs) )

    @staticmethod
    def new(*,mode,size,**kwargs):
        from PIL import Image as PImage
        return Image( pil=PImage.new(mode=mode,size=size,**kwargs) )
   
# Import all functions.
from .purify import *


