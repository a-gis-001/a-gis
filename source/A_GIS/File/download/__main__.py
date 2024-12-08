import A_GIS.File.download
import sys
import pathlib

for z in sys.argv[1:]:
    A_GIS.File.download(url=z,output_folder=pathlib.Path('.'),filename='download')
