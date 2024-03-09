import A_GIS.Code.Unit.move
import A_GIS.Code.Unit.find_root
import sys
import pathlib

old = pathlib.Path(sys.argv[1])
new = pathlib.Path(sys.argv[2])
A_GIS.Code.Unit.move(root=A_GIS.Code.Unit.find_root(path=old), old=old, new=new)
