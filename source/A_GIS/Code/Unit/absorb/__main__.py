import A_GIS.Code.Unit.absorb
import A_GIS.File.read
import A_GIS.Code.highlight
import sys

code = A_GIS.File.read(file=sys.argv[1])

code=A_GIS.Code.Unit.absorb(code=code, name='A_GIS.Feelings.draw')

print(A_GIS.Code.highlight(code=code))
