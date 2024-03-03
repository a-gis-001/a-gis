def main():
    import A_GIS.Code.Tree
    import sys
    import pathlib

    tree = A_GIS.Code.Tree.recurse(path=pathlib.Path(sys.argv[1]))
    print(A_GIS.Code.Tree.print(tree=tree))

    A_GIS.Code.Tree.update(tree=tree)

    print(A_GIS.Code.Tree.print(tree=tree))


if __name__ == "__main__":
    main()
