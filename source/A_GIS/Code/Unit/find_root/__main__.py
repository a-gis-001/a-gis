import A_GIS.Code.Unit.find_root
import sys
import pathlib

if len(sys.argv) > 1:
    file = sys.argv[1]
else:
    file = sys.argv[0]
print(A_GIS.Code.Unit.find_root(path=pathlib.Path(file)))
