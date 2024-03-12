def plot(
    *,
    distributions=None,
    realizations=None,
    alpha=0.5,
    labels=None,
    ax=None,
    min_val=None,
    max_val=None,
    space=100,
    bins=20,
    density=True,
    colors=None,
    weights=None,
):
    """
    Plot realizations and PDFs of distributions on the given axis with specified or default colors.

    Parameters:
    - distributions: List of distribution objects with a .pdf method.
    - realizations: numpy.ndarray containing sampled realizations.
    - ax: matplotlib axis object to plot on.
    - min_val, max_val: float, range of x-axis.
    - space: int, number of points to calculate PDF.
    - bins: int, number of bins for histogram.
    - density: bool, if True, normalize histograms.
    - colors: Optional[List[str]], colors for the histogram and PDF lines. If None, a default set is used.
    """
    import numpy
    import matplotlib.pyplot

    # Get number of distributions from either variable
    ndist = 0
    has_distributions = False
    has_realizations = False
    if distributions is not None:
        ndist = len(distributions)
        has_distributions = True
    if realizations is not None:
        ndist = len(realizations.T)
        has_realizations = True
    if not (has_distributions or has_realizations):
        raise ValueError("Must have distributions or realizations")

    if ax is None:
        fig, ax = matplotlib.pyplot.subplots()

    if weights is None:
        weights = [1.0] * ndist

    if labels is None:
        labels = [f"Dist {i+1}" for i in range(ndist)]

    # Use a default set of colors from Matplotlib's cycle or a provided list
    if colors is None:
        color_cycle = matplotlib.pyplot.rcParams["axes.prop_cycle"].by_key()[
            "color"
        ]  # Default Matplotlib color cycle
        colors = [color_cycle[i % len(color_cycle)] for i in range(ndist)]

    # Add important values.
    critical_vals = []
    if has_realizations:
        min_val = numpy.min(realizations)
        max_val = numpy.max(realizations)
    if has_distributions:
        for d in distributions:
            critical_vals.extend([d.mode, d.low, d.high])
        min_val = numpy.min(critical_vals)
        max_val = numpy.max(critical_vals)

    # Get x-axis values
    x_vals = numpy.linspace(min_val, max_val, space)
    if len(critical_vals) > 0:
        x_vals = numpy.sort(numpy.append(x_vals, critical_vals))

    for i in range(ndist):  # Iterate through each set of realizations
        color = colors[i]  # Color for the current distribution
        # Plot histogram of realizations with specified/default color
        if has_realizations:
            ax.hist(
                realizations.T[i],
                bins=bins,
                density=density,
                alpha=alpha,
                color=color,
                edgecolor=color,
            )
        # Plot PDF of corresponding distribution with specified/default color
        if has_distributions:
            pdf_vals = [distributions[i].pdf(x) for x in x_vals]
        ax.plot(x_vals, pdf_vals, label=labels[i], color=color)
        ax.set_xlim([min_val, max_val])

    ax.legend()
    return ax
