def plot_halflife(*, data, timestamp=None, label='Enhancement', projections_after=None, target_halflife=120., projections_after_label='Projections after'):
    
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

    if not projections_after:
       projections_after = A_GIS.Dev.Metrics.get_dates(data=data, key='closed_at', label=label)[-1]

    dates, half_lives = A_GIS.Dev.Metrics.calculate_halflife(data=data, label=label, projections_after=projections_after)

    # Create a plot for the half-life data
    fig, ax = matplotlib.pyplot.subplots(figsize=(10, 6))
    A_GIS.Visual.plot_transition(
        dates=dates,
        y_values=half_lives,
        target_date=projections_after,
        plot_function=ax.plot,
        label="Half-life",
        pre_style={"color": "blue", "alpha": 0.6},
        post_style={"color": "black", "alpha": 0.4, "linestyle": "--"},
    )

    # Plot closure dates with different styling
    A_GIS.Visual.plot_transition(
        dates=dates,
        y_values=half_lives,
        target_date=projections_after,
        plot_function=ax.plot,
        label="Closure dates",
        pre_style={
            "color": "blue",
            "alpha": 0.2,
            "marker": ".",
            "markersize": 10,
        },
        post_style={
            "color": "black",
            "alpha": 0.1,
            "marker": ".",
            "markersize": 10,
        },
    )

    # Plot a target line for reference
    ax.plot(
        dates,
        [target_halflife / 365.25] * len(dates),
        alpha=0.5,
        linewidth=4,
        label="Target",
        color="green",
        linestyle="-",
    )

    # Add a vertical line indicating the last issue closed
    ax.axvline(
        projections_after,
        color="blue",
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
