import A_GIS.Code.Unit.get
import A_GIS.Code.Unit.to_string
import A_GIS.Code.Unit.check
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
    # print(unit)
    msg = A_GIS.Code.Unit.check(unit=unit)
    if msg == []:
        print(f"File {z} passes check!")
    else:
        for m in msg:
            print(m)
        print(f"Full file {z}")
        print(A_GIS.Code.Unit.to_string(unit=unit))
