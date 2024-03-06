import A_GIS.Code.touch
import sys
import pathlib
import subprocess
import os

if len(sys.argv) == 1:
    start = 0
else:
    start = 1
    
for z in sys.argv[start:]:
    path = A_GIS.Code.touch(path=pathlib.Path(z))
    if 'EDITOR' in os.environ:
        subprocess.run([os.environ.get('EDITOR'), str(path)])
