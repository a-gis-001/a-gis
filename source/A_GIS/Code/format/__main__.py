import A_GIS.Code.touch
import A_GIS.Code.format
import A_GIS.File.read
import A_GIS.File.write
import sys
import pathlib
import subprocess

for z in sys.argv[1:]:
    path = A_GIS.Code.touch(path=pathlib.Path(z))
    code = A_GIS.File.read(path=path)
    formatted_code = A_GIS.Code.format(code=code)
    A_GIS.File.write(content=formatted_code,file=path)

