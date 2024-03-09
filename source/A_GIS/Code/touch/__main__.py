import A_GIS.Code.touch
import A_GIS.Code.Unit.find_root
import A_GIS.Code.to_path
import sys
import pathlib
import subprocess
import os

if len(sys.argv) == 1:
    start = 0
else:
    start = 1
    
root = A_GIS.Code.Unit.find_root(path=pathlib.Path(sys.argv[0]))
for z in sys.argv[start:]:
    if '.' in z: 
        path = A_GIS.Code.to_path(name=z)
        path = root.parent / path
    else:
        path = pathlib.Path(z).resolve()
    print(path.relative_to(path.cwd()))
    path = A_GIS.Code.touch(path=path)
    if 'EDITOR' in os.environ:
       subprocess.run([os.environ.get('EDITOR'), str(path)])
