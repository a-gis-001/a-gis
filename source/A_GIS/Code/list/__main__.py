import sys
import A_GIS.Code.list
import json

result = A_GIS.Code.list()
print(json.dumps({
    "modules": result.modules,
    "functions": result.functions
}, indent=4))
