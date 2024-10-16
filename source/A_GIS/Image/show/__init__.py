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
    **kwargs,
):
    """Show an image for convenience and profit."""
    import numpy
    import matplotlib.pyplot
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
    fig, ax = matplotlib.pyplot.subplots(figsize=(figsize, figsize))

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
    if grid:
        radius = math.sqrt(wh_scale[0] * wh_scale[1])
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

    # Adjust margins while keeping ticks and labels
    fig.subplots_adjust(
        left=0.02, right=0.98, top=0.98, bottom=0.02
    )  # Adjust to reduce whitespace
    ax.margins(0, 0)  # Remove additional axes margins

    # Display the image with reduced margins
    ax.imshow(image, **kwargs)

    buf = io.BytesIO()
    fig.savefig(
        buf, format="jpeg", bbox_inches="tight", pad_inches=0.1, dpi=dpi
    )  # Save without excess padding
    buf.seek(0)
    plot_image = PIL.Image.open(buf)

    if show:
        matplotlib.pyplot.show()

    if close:
        matplotlib.pyplot.close(fig)
        fig = None

    return A_GIS.Code.make_struct(image=plot_image, figure=fig, _image=image)
