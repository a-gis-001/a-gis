import A_GIS.Code.split
import A_GIS.File.read
import sys

s=A_GIS.Code.split(code=A_GIS.File.read(file=sys.argv[1]))

for k,v in s.items():
    print(k)
    print(v)
    print('---')
