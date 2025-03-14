import A_GIS.Code.Unit.touch
import A_GIS.Code.reformat
import A_GIS.File.read
import A_GIS.File.write
import sys
import pathlib
import subprocess

for z in sys.argv[1:]:
    file=pathlib.Path(z)
    code = A_GIS.File.read(file=file)
    formatted_code = A_GIS.Code.reformat(code=code)
    A_GIS.File.write(content=formatted_code, file=file)
