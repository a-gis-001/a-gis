import A_GIS.Code.Unit.touch
import sys
import pathlib
import subprocess
import os

if len(sys.argv) == 1:
    start = 0
else:
    start = 1

for name in sys.argv[start:]:
    path = A_GIS.Code.Unit.touch(name=name)
    if "EDITOR" in os.environ:
        subprocess.run([os.environ.get("EDITOR"), str(path)])
