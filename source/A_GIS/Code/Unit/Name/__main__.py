import sys
import A_GIS.Code.Unit.Name.generate

x = A_GIS.Code.Unit.Name.generate(description=sys.argv[1])

print(x.content)
print("\n\n\n")

for n in x.names:
    print(f"- {n}")
