import A_GIS.Code.convert_multiline
import A_GIS.File.read
import A_GIS.File.write
import sys

for file in sys.argv[1:]:
    code = A_GIS.File.read(file=file)
    code = A_GIS.Code.convert_multiline(code=code)
    print(code)
