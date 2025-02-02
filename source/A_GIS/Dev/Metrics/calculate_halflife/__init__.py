def calculate_halflife(
    *,
    data,
    start_date=None,
    end_date=None,
    label="Enhancement",
    projections_after=None,
):
    """Calculate the half-life of issues based on issue closure statistics.

    Args:
        data (dict): The issue data containing `started_at` and `closed_at` dates.

    Returns:
        tuple: A tuple containing lists of dates and their corresponding half-lives.
    """
    import numpy
    import A_GIS.Dev.Metrics.get_closure_stats
    import A_GIS.Time.get

    # Define the date range for closure statistics
    # TODO update this to be based on the first/last date in the data.
    if not start_date:
        start_date = A_GIS.Time.get(year=2018)
    if not end_date:
        end_date = A_GIS.Time.get(year=2050)

    # Get closure statistics within the specified date range
    stats, all_issues = A_GIS.Dev.Metrics.get_closure_stats(
        data=data,
        start_date=start_date,
        label=label,
        end_date=end_date,
        projections_after=projections_after,
    )

    # Initialize lists to store dates and half-lives
    dates = []
    half_lives = []

    # Calculate half-life for each closure statistic point
    last_date = None
    for point in stats:
        last_date = point[0]
        closure_counts = numpy.array(point[2])
        fractions = closure_counts / (1e-20 + closure_counts[0])
        index = (
            numpy.argmax(fractions < 0.5)
            if numpy.any(fractions < 0.5)
            else None
        )
        if index is not None:
            dates.append(point[0])
            half_lives.append(
                point[1][index] / 365.25
            )  # Convert days to years
    dates.append(last_date)
    half_lives.append(0.0)
    return dates, half_lives, all_issues
