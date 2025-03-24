def _draw_clock_face(
    *,
    ax,
    face: "A_GIS.Visual.Clock._Face",
    radius=0.4,
    center=(0, 0),
    marker_length=0.08,
):
    """Draw a clock face with hour markers.

    Args:
        ax: Matplotlib axes to draw on
        face: Face parameters from init_face()
        radius: Radius of the clock face (default 0.4)
        center: Center point of the clock (default (0, 0))
        marker_length: Length of hour markers (default 0.08)
    """
    import matplotlib.pyplot
    import numpy

    # Draw the outer circle
    circle = matplotlib.pyplot.Circle(
        center, radius, fill=False, color=face.edge_color, linewidth=face.edge_width
    )
    ax.add_patch(circle)

    # Draw hour markers
    for hour in range(12):
        angle = numpy.pi / 2 - (hour * numpy.pi / 6)  # Start from 12 o'clock

        # Calculate marker start and end points
        outer_r = radius
        inner_r = radius - marker_length

        x1 = center[0] + outer_r * numpy.cos(angle)
        y1 = center[1] + outer_r * numpy.sin(angle)
        x2 = center[0] + inner_r * numpy.cos(angle)
        y2 = center[1] + inner_r * numpy.sin(angle)

        # Draw the hour marker
        ax.plot([x1, x2], [y1, y2], color=face.tick_color, linewidth=face.tick_width)

    # Set equal aspect ratio and remove axes
    ax.set_aspect("equal")
    matplotlib.pyplot.axis("off")
