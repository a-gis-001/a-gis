import A_GIS.File.read
import sys
import A_GIS.Code.highlight
import A_GIS.Code.rename_function

code=A_GIS.Code.rename_function(
    code=A_GIS.File.read(
        file=sys.argv[1]
    ),
    old=sys.argv[2],
    new=sys.argv[3]
)

print(A_GIS.Code.highlight(code=code))
