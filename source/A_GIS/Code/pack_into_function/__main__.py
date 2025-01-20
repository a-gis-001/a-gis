import A_GIS.Code.pack_into_function
import A_GIS.File.read
import sys
import A_GIS.Code.highlight

s=A_GIS.Code.pack_into_function(
    code=A_GIS.File.read(
        file=sys.argv[1]
    )
)

print(A_GIS.Code.highlight(code=s.code))
