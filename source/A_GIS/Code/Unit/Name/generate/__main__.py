import sys
import A_GIS.Code.Unit.Name.generate

# Try three times.
names = []
for n in A_GIS.Code.Unit.Name.generate(
    description=sys.argv[1], temperature=0.9, tries=3
):
    print(n)
    if len(n) > len("A_GIS."):
        names.append(n)

print(
    A_GIS.Code.Unit.Name.generate(
        description=sys.argv[1], suggestions=names, temperature=0.5
    )
)
