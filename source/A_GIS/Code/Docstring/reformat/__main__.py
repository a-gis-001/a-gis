import A_GIS.Code.Docstring.reformat
import A_GIS.Code.Docstring.clean
import A_GIS.Code.parse_docstring
import A_GIS.Code.replace_docstring
import A_GIS.File.read
import A_GIS.File.write
import sys

for arg in sys.argv[1:]:
    code = A_GIS.File.read(file=arg)
    text = A_GIS.Code.parse_docstring(code=code)
    text = A_GIS.Code.Docstring.clean(docstring=text)
    docstring = A_GIS.Code.Docstring.init(text=text,reference_code=code)
    docstring = A_GIS.Code.Docstring.reformat(docstring=docstring)
    code = A_GIS.Code.replace_docstring(code=code, docstring=docstring)
    A_GIS.File.write(content=code, file=arg)
