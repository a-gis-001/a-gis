import A_GIS.Code.Unit.get
import A_GIS.Code.Unit.to_string
import sys
import A_GIS.File.read
import pathlib

if len(sys.argv) == 1:
    start = 0
else:
    start = 1

y = [pathlib.Path(x) / "__init__.py" for x in sys.argv]

for z in y[start:]:
    unit = A_GIS.Code.Unit.get(code=A_GIS.File.read(file=z))
    print(A_GIS.Code.Unit.to_string(unit=unit))
