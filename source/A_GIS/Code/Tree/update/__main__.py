import A_GIS.Code.Tree.recurse
import A_GIS.Code.Tree.print
import A_GIS.Code.Tree.update
import pathlib
import sys

root = A_GIS.Code.find_root(path=pathlib.Path(sys.argv[0]))
tree = A_GIS.Code.Tree.recurse(path=root)
print(A_GIS.Code.Tree.print(tree=tree))

A_GIS.Code.Tree.update(tree=tree)

print(A_GIS.Code.Tree.print(tree=tree))
