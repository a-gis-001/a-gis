import A_GIS.Code.Unit.absorb
import A_GIS.File.read
import A_GIS.Code.highlight
import sys

x=A_GIS.Code.Unit.absorb(
    code=A_GIS.File.read(
        file=sys.argv[1]
    ),
    write=False
)

print(x.name)
print(A_GIS.Code.highlight(code=x.code))
