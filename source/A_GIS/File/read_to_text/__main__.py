import A_GIS.File.read_to_text
import sys
import pathlib

for z in sys.argv[1:]:
    print(
        A_GIS.File.read_to_text(file=pathlib.Path(z))
    )
