import A_GIS.File.read_to_text
import sys
import pathlib
import A_GIS.File.is_url

dirs=[]
for z in sys.argv[1:]:
    if A_GIS.File.is_url(name=z):
        path=z
    else:
        path=pathlib.Path(z)
    print(
        A_GIS.File.read_to_text(path=path)
    )