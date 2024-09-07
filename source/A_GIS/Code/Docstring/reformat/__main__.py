import A_GIS.Code.Docstring.reformat
import A_GIS.Code.get_docstring
import A_GIS.Code.replace_docstring
import A_GIS.File.read
import A_GIS.File.write
import sys

for file in sys.argv[1:]:
    code = A_GIS.File.read(file=file)
    docstring = A_GIS.Code.get_docstring(code=code)
    docstring = A_GIS.Code.Docstring.reformat(docstring=docstring)
    code = A_GIS.Code.replace_docstring(code=code, docstring=docstring)
    A_GIS.File.write(content=code, file=file)
