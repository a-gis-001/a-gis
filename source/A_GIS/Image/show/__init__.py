def show(
    *,
    image,
    wh_scale=[1, 1],
    xlabel="w [-]",
    ylabel="h [-]",
    figsize=10,
    grid=False,
    nticks=5,
    nlabels=2,
    show=True,
    dpi=400,
    close=True,
    boxes=None,
    **kwargs,
):
    """Show an image for convenience and profit."""
    import numpy
    import matplotlib.pyplot
    import matplotlib.patches
    import io
    import PIL
    import A_GIS.Code.make_struct
    import math

    if image is None:
        return A_GIS.Code.make_struct(image=None, figure=None, _image=None)

    # Ensure valid values for nticks and nticklabels
    if nticks <= 0:
        raise ValueError("nticks must be greater than 0.")
    if nlabels <= 1:
        raise ValueError("nlabels must be greater than 1.")

    # Set up plot with modified axes based on character size
    w, h = image.size
    pw = w * figsize / h
    ph = figsize
    fig, ax = matplotlib.pyplot.subplots(figsize=(pw, ph))

    data = numpy.array(image)

    height, width = data.shape[:2]
    # Set major and minor ticks
    x_major_ticks = numpy.arange(0, width, wh_scale[0] * nticks * nlabels)
    y_major_ticks = numpy.arange(0, height, wh_scale[1] * nticks * nlabels)
    x_minor_ticks = numpy.arange(0, width, wh_scale[0] * nticks)
    y_minor_ticks = numpy.arange(0, height, wh_scale[1] * nticks)

    # Set major and minor ticks
    ax.set_xticks(x_major_ticks)
    ax.set_yticks(y_major_ticks)
    ax.set_xticks(x_minor_ticks, minor=True)
    ax.set_yticks(y_minor_ticks, minor=True)

    # Set automatic tick labels for major ticks
    ax.set_xticklabels([int(x / wh_scale[0]) for x in x_major_ticks])
    ax.set_yticklabels([int(y / wh_scale[1]) for y in y_major_ticks])

    # Set labels
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Add a light dotted grid for minor ticks and darker grid for major ticks
    radius = math.sqrt(wh_scale[0] * wh_scale[1])
    if grid:
        ax.grid(
            which="major",
            linestyle="-",
            linewidth=min(2.0, 0.1 * radius),
            color="grey",
            alpha=0.2,
        )
        ax.grid(
            which="minor",
            linestyle=":",
            linewidth=min(1.0, 0.05 * radius),
            color="grey",
            alpha=0.2,
        )

    ax.margins(0, 0)  # Remove additional axes margins

    # Draw bounding boxes if provided
    if boxes is not None:
        for box in boxes:
            ul_x, ul_y = box[0]  # Upper-left corner coordinates
            lr_x, lr_y = box[1]  # Lower-right corner coordinates
            color = box[2]
            linewidth = box[3] if len(box) >= 4 else 0.1 * radius
            bw = lr_x - ul_x
            bh = lr_y - ul_y
            sw = wh_scale[0]
            sh = wh_scale[1]
            ax.plot(
                ul_x * sw,
                ul_y * sh,
                marker="o",
                color=color,
                markersize=5 * linewidth,
            )
            rect = matplotlib.patches.Rectangle(
                (ul_x * sw, ul_y * sh),
                bw * sw,
                bh * sh,
                linewidth=linewidth,
                edgecolor=color,
                facecolor="none",
            )
            ax.add_patch(rect)

    # Display the image with reduced margins
    ax.imshow(image, **kwargs)

    buf = io.BytesIO()
    fig.savefig(
        buf, format="jpeg", bbox_inches="tight", pad_inches=0.0, dpi=dpi
    )  # Save without excess padding
    buf.seek(0)
    plot_image = PIL.Image.open(buf)

    if show:
        matplotlib.pyplot.show()

    if close:
        matplotlib.pyplot.close(fig)
        fig = None

    return A_GIS.Code.make_struct(image=plot_image, figure=fig, _image=image)
