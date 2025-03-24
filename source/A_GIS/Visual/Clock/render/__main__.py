import argparse
import matplotlib.pyplot
import A_GIS.Visual.Clock.render


parser = argparse.ArgumentParser(description="Render a clock face with specified time")
parser.add_argument("hour", type=int, help="Hour (0-23)")
parser.add_argument("minute", type=int, help="Minute (0-59)")
parser.add_argument("second", type=int, help="Second (0-59)")

args = parser.parse_args()
print(f"Arguments received: hour={args.hour}, minute={args.minute}, second={args.second}")

print("Rendering clock...")
result = A_GIS.Visual.Clock.render(
    hour=args.hour,
    minute=args.minute,
    second=args.second,
)

if result.error:
    print(f"Error: {result.error}")
else:
    print("Displaying clock...")
    matplotlib.pyplot.imshow(result.image)
    matplotlib.pyplot.axis("off")
    matplotlib.pyplot.show()
