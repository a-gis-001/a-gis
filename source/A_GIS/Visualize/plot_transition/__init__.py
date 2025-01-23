def plot_transition(
    dates,
    y_values,
    target_date,
    plot_function,
    label,
    pre_style,
    post_style,
    pre_annotation=" (Actual)",
    post_annotation=" (Projection)",
    **kwargs,
):
    """
    Generalized plotting function with a style change at a target date.

    Parameters:
        dates (array-like): Array of datetime objects representing the x-axis values.
        y_values (tuple or array-like): Single y-values (e.g., for plt.plot) or a tuple of (y1, y2) for fill_between.
        target_date (datetime): Date at which the plot style changes.
        plot_function (function): The Matplotlib plotting function (e.g., plt.plot, plt.fill_between).
        label (str): Label for the plot or fill.
        pre_style (dict): Dictionary of plotting style for dates <= target_date.
        post_style (dict): Dictionary of plotting style for dates > target_date.
        **kwargs: Additional arguments passed to the plotting function.
    """
    import numpy as np
    import numpy as np

    # Convert inputs to numpy arrays for indexing
    dates = np.array(dates)

    # Boolean masks for pre- and post-target dates
    pre_mask = dates <= target_date
    post_mask = dates > target_date

    if isinstance(y_values, tuple):
        # Handle multiple y-values (e.g., for fill_between)
        y1, y2 = y_values
        y1 = np.array(y1)
        y2 = np.array(y2)

        # Plot the pre-target segment
        plot_function(
            dates[pre_mask],
            y1[pre_mask],
            y2[pre_mask],
            label=f"{label}{pre_annotation}",
            **pre_style,
            **kwargs,
        )
        # Plot the post-target segment
        plot_function(
            dates[post_mask],
            y1[post_mask],
            y2[post_mask],
            label=f"{label}{post_annotation}",
            **post_style,
            **kwargs,
        )
    else:
        # Handle single y-values (e.g., for plt.plot)
        y_values = np.array(y_values)

        # Plot the pre-target segment
        plot_function(
            dates[pre_mask],
            y_values[pre_mask],
            label=f"{label}{pre_annotation}",
            **pre_style,
            **kwargs,
        )
        # Plot the post-target segment
        plot_function(
            dates[post_mask],
            y_values[post_mask],
            label=f"{label}{post_annotation}",
            **post_style,
            **kwargs,
        )
