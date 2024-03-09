import sys
import A_GIS.Code.name

# Try three times.
names = A_GIS.Code.name(description=sys.argv[1],tries=3)

print(
	A_GIS.Code.name(description=sys.argv[1]+"\n Suggestions are: "+",".join(names))
)