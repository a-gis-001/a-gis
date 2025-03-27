def _draw_clock_face(
    *,
    ax,
    face: "A_GIS.Visual.Clock._Face" = None,
):
    """Draw a clock face with hour markers and optional minute markers.

    Args:
        ax: Matplotlib axes to draw on
        face: Face parameters from init_face()
    """
    import matplotlib.pyplot
    import numpy
    import A_GIS.Visual.Clock.init_face

    radius = 1.0
    center = (0, 0)

    if face is None:
        face = A_GIS.Visual.Clock.init_face()

    errors = []
    if face.error:
        errors.append(face.error)

    if errors:
        return "\n".join(errors)

    # Set axis limits to show the full clock face
    ax.set_xlim(-1.2, 1.2)  # Add some padding
    ax.set_ylim(-1.2, 1.2)  # Add some padding

    # Draw the outer circle
    circle = matplotlib.pyplot.Circle(
        center, radius, 
        facecolor=face.color,  # Use facecolor instead of fill
        edgecolor=face.edge_color,  # Use edgecolor instead of color
        linewidth=face.edge_width
    )
    ax.add_patch(circle)

    # Draw hour markers
    for hour in range(12):
        angle = numpy.pi / 2 - (hour * numpy.pi / 6)  # Start from 12 o'clock

        # Calculate marker start and end points
        outer_r = radius
        inner_r = radius - face.hour_marker_length

        x1 = center[0] + outer_r * numpy.cos(angle)
        y1 = center[1] + outer_r * numpy.sin(angle)
        x2 = center[0] + inner_r * numpy.cos(angle)
        y2 = center[1] + inner_r * numpy.sin(angle)

        # Draw the hour marker
        ax.plot([x1, x2], [y1, y2], color=face.tick_color, linewidth=face.tick_width)

    # Draw minute markers if enabled
    if face.minute_marker_factor > 0:
        minute_marker_length = face.hour_marker_length * face.minute_marker_factor
        for minute in range(60):
            angle = numpy.pi / 2 - (minute * numpy.pi / 30)  # Start from 12 o'clock

            # Calculate marker start and end points
            outer_r = radius
            inner_r = radius - minute_marker_length

            x1 = center[0] + outer_r * numpy.cos(angle)
            y1 = center[1] + outer_r * numpy.sin(angle)
            x2 = center[0] + inner_r * numpy.cos(angle)
            y2 = center[1] + inner_r * numpy.sin(angle)

            # Draw the minute marker
            ax.plot([x1, x2], [y1, y2], color=face.tick_color, linewidth=face.tick_width)

    # Draw numbers if enabled
    if face.number_mode != 'none':
        # Calculate which hours to draw
        hours_to_draw = range(1, 13) if face.number_mode == 'all' else [12, 3, 6, 9]
        
        for hour in hours_to_draw:
            angle = numpy.pi / 2 - ((hour % 12) * numpy.pi / 6)  # Start from 12 o'clock
            
            # Position numbers slightly inside the markers
            number_r = radius - face.hour_marker_length - face.number_size * 0.5
            
            x = center[0] + number_r * numpy.cos(angle)
            y = center[1] + number_r * numpy.sin(angle)
            
            # Adjust text alignment based on position
            ha = 'center'
            va = 'center'
            if hour in [3, 9]:
                ha = 'left' if hour == 3 else 'right'
            elif hour in [6, 12]:
                va = 'top' if hour == 12 else 'bottom'
            
            ax.text(x, y, str(hour), 
                   fontsize=face.number_size * 100,  # Scale to reasonable size
                   fontfamily=face.number_font,
                   ha=ha, va=va,
                   color=face.tick_color)

    # Set equal aspect ratio and remove axes
    ax.set_aspect("equal")
    matplotlib.pyplot.axis("off")
