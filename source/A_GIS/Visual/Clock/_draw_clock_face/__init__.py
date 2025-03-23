def _draw_clock_face(*, ax, radius=0.4, center=(0.5, 0.5), marker_length=0.08, color='black', linewidth=2):
    """Draw a clock face with hour markers.
    
    Args:
        ax: Matplotlib axes to draw on
        radius: Radius of the clock face (default 0.4)
        center: Center point of the clock (default (0.5, 0.5))
        marker_length: Length of hour markers (default 0.08)
        color: Color of the clock face and markers (default 'black')
        linewidth: Width of lines (default 2)
    """
    import matplotlib.pyplot
    import numpy
    
    # Draw the outer circle
    circle = matplotlib.pyplot.Circle(center, radius, fill=False, color=color, linewidth=linewidth)
    ax.add_patch(circle)
    
    # Draw hour markers
    for hour in range(12):
        angle = numpy.pi/2 - (hour * numpy.pi/6)  # Start from 12 o'clock
        
        # Calculate marker start and end points
        outer_r = radius
        inner_r = radius - marker_length
        
        x1 = center[0] + outer_r * numpy.cos(angle)
        y1 = center[1] + outer_r * numpy.sin(angle)
        x2 = center[0] + inner_r * numpy.cos(angle)
        y2 = center[1] + inner_r * numpy.sin(angle)
        
        # Draw the hour marker
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=linewidth)
    
    # Set equal aspect ratio and remove axes
    ax.set_aspect('equal')
    matplotlib.pyplot.axis('off') 