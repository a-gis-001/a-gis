import A_GIS.Code.Unit.rename
import sys
import pathlib

A_GIS.Code.Unit.rename(
    root=pathlib.Path(sys.argv[1]),
    old=pathlib.Path(sys.argv[2]),
    new=pathlib.Path(sys.argv[3])
)
