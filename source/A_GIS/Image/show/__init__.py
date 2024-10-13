def show(
    *,
    image,
    xy_scale=[1, 1],
    xlabel="x [-]",
    ylabel="y [-]",
    figsize=10,
    grid=False,
    nticks=5,
    nlabels=2,
    show=True,
    dpi=400,
    **kwargs,
):
    """Show an image for convenience and profit."""
    import numpy
    import matplotlib.pyplot
    import io
    import PIL
    import A_GIS.Code.make_struct

    # Ensure valid values for nticks and nticklabels
    if nticks <= 0:
        raise ValueError("nticks must be greater than 0.")
    if nlabels <= 1:
        raise ValueError("nlabels must be greater than 1.")
    nticklabels = nlabels * nticks

    # Set up plot with modified axes based on character size
    fig, ax = matplotlib.pyplot.subplots(figsize=(figsize, figsize))

    data = numpy.array(image)

    height, width = data.shape[:2]
    # Set ticks every nticks * xy_scale
    x_ticks = numpy.arange(0, width, xy_scale[0] * nticks)
    y_ticks = numpy.arange(0, height, xy_scale[1] * nticks)

    # Set ticks every nticks
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)

    # Set labels every nticklabels
    ax.set_xticklabels(
        [
            (
                ""
                if (nticklabels // nticks) == 0
                or i % (nticklabels // nticks) != 0
                else int(x / xy_scale[0])
            )
            for i, x in enumerate(x_ticks)
        ]
    )
    ax.set_yticklabels(
        [
            (
                ""
                if (nticklabels // nticks) == 0
                or i % (nticklabels // nticks) != 0
                else int(y / xy_scale[1])
            )
            for i, y in enumerate(y_ticks)
        ]
    )

    # Set labels
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Add a light dotted grid
    if grid:
        ax.grid(
            which="both", linestyle=":", linewidth=0.5, color="gray", alpha=0.5
        )

    # Adjust margins while keeping ticks and labels
    fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)  # Adjust to reduce whitespace
    ax.margins(0, 0)  # Remove additional axes margins

    # Display the image with reduced margins
    ax.imshow(image, **kwargs)

    buf = io.BytesIO()
    fig.savefig(buf, format='jpeg', bbox_inches='tight', pad_inches=0.1, dpi=dpi)  # Save without excess padding
    buf.seek(0)
    plot_image = PIL.Image.open(buf)

    if show:
        matplotlib.pyplot.show()

    return A_GIS.Code.make_struct(image=plot_image, figure=fig, _image=image)
