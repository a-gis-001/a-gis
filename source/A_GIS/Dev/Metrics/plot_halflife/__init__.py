def plot_halflife(
    *,
    data,
    timestamp=None,
    label="Enhancement",
    pre_color="blue",
    post_color="black",
    target_color="green",
    projections_after=None,
    target_halflife=120.0,
    projections_after_label="Last actual",
    start_date=None,
    end_date=None,
):
    """Calculate and return a plot object for the half-life of enhancements over time.

    This function calculates the half-life of issues with label issue closure statistics
    and returns a plot object that can be modified or displayed by the user.

    Args:
        data (dict): The issue data containing `started_at` and `closed_at` dates.
        timestamp (datetime, optional): A timestamp for saving the plot with a specific name.

    Returns:
        matplotlib.figure.Figure: A matplotlib figure object containing the plot.
    """
    import A_GIS.Dev.Metrics.calculate_halflife
    import A_GIS.Dev.Metrics._get_completed
    import matplotlib.pyplot
    import datetime
    import A_GIS.Visual.plot_transition

    closed_dates = A_GIS.Dev.Metrics.get_dates(
        data=data, key="closed_at", label=label
    )
    started_dates = A_GIS.Dev.Metrics.get_dates(
        data=data, key="started_at", label=label
    )
    if not projections_after:
        projections_after = closed_dates[-1]

    dates, half_lives, all_issues = A_GIS.Dev.Metrics.calculate_halflife(
        data=data,
        label=label,
        projections_after=projections_after,
        start_date=start_date,
        end_date=end_date,
    )

    # Create a plot for the half-life data
    fig, ax = matplotlib.pyplot.subplots(figsize=(10, 6))
    A_GIS.Visual.plot_transition(
        dates=dates,
        y_values=half_lives,
        target_date=projections_after,
        plot_function=ax.plot,
        label="Half-life",
        pre_annotation=" (Actual+Projected)",
        post_annotation=" (Projected)",
        pre_style={"color": pre_color, "alpha": 0.6},
        post_style={"color": post_color, "alpha": 0.4, "linestyle": "--"},
    )

    # Plot started dates.
    ax.plot(
        started_dates,
        [target_halflife / 365.25] * len(started_dates),
        alpha=0.3,
        linewidth=4,
        label="Started date",
        color=target_color,
        marker=".",
        markersize=10,
        linestyle="",
    )

    # Plot closed dates.
    ax.plot(
        closed_dates,
        [0.0] * len(closed_dates),
        alpha=0.3,
        linewidth=4,
        label="Closed date",
        color=post_color,
        marker=".",
        markersize=10,
        linestyle="",
    )

    for issue in all_issues:
        ax.plot(
            # x-coordinates (time range)
            [issue["started_at"], issue["closed_at"]],
            # y-coordinates (fixed y-values for start and end)
            [target_halflife / 365.25, 0.0],
            marker="",  # Add markers to show start and end points
            linestyle="-",
            color=post_color,
            alpha=0.9,
            linewidth=0.2,
            label="_nolegend_",  # Prevent this line from appearing in the legend
        )

    # Plot a target line for reference
    ax.axhline(
        target_halflife / 365.25,
        alpha=0.5,
        linewidth=4,
        label="Target half-life",
        color=target_color,
        linestyle="-",
    )

    # Add a vertical line indicating the last issue closed
    ax.axvline(
        projections_after,
        color=post_color,
        linestyle="--",
        label=projections_after_label,
    )

    # Add labels, legend, and grid to the plot
    ax.set_ylabel("Half-life (years)")
    ax.set_xlabel("Date")
    ax.set_title(f"{label} Half-life")
    ax.legend(loc="upper right")
    ax.grid(True, linestyle="--", alpha=0.7)
    fig.tight_layout()

    matplotlib.pyplot.close(fig)

    return fig
