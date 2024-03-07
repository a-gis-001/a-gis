import A_GIS.Code.highlight
import A_GIS.File.read
import sys
import pathlib

for z in sys.argv[1:]:
    print(
        A_GIS.Code.highlight(
            code=A_GIS.File.read(
                file=A_GIS.Code.touch(
                    path=pathlib.Path(z)
                )
            )
        )
    )

