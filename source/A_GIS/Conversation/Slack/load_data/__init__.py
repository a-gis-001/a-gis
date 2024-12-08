def load_data(*, directory, channel, date, adjacent_range=[-0.5, 0.5]):
    import pathlib
    import A_GIS.Code.make_struct
    import datetime
    import json

    def load_messages(file):
        with open(file, "r") as f:
            return extract_messages(json.load(f))

    def extract_indices(text):
        import re

        pattern = r"\n\s*parts:\s*([0-9, \-]+)"
        match = re.search(pattern, text.lower())

        indices = []
        if match:
            # This should be something like "0,-1"
            indices_str = match.group(1)
            # Split by comma and convert to integers
            indices = [int(x.strip()) for x in indices_str.split(",")]
        return indices

    def extract_messages(data):
        import pytz

        est = pytz.timezone("US/Eastern")  # Define Eastern Standard Time
        messages = []
        for message in data:
            ts = float(message["ts"])
            user = message.get("user", "Unknown")
            text = message.get("text", "")
            utc_time = datetime.datetime.utcfromtimestamp(ts).replace(
                tzinfo=pytz.utc
            )
            est_time = utc_time.astimezone(est)
            timestamp = est_time.strftime("%Y-%m-%d %H:%M:%S")
            messages.append((timestamp, user, text))
        messages.sort()
        return messages

    def get_filename(d0, channel, date):
        return pathlib.Path(str(d0 / channel / date) + ".json")

    def find_adjacent(d0, channel, date, delta):
        """
        Find the adjacent file based on the given delta from the date.

        Args:
            d0 (Path or str): Base directory.
            channel (str): Channel name.
            date (str): Date in 'YYYY-MM-DD' format.
            delta (int): Number of days to move forward or backward.

        Returns:
            Path or None: The path to the adjacent file if found, otherwise None.
        """
        if not isinstance(delta, int):
            raise ValueError("delta must be an integer.")

        current_date = datetime.datetime.strptime(date, "%Y-%m-%d")
        step = -1 if delta < 0 else 1  # Determine the direction of iteration

        for i in range(abs(int(delta))):
            # Calculate the next date to check
            next_date = current_date + datetime.timedelta(days=step * (i + 1))
            next_date_str = next_date.strftime("%Y-%m-%d")

            # Generate the filename and check if it exists
            candidate_file = get_filename(d0, channel, next_date_str)
            if candidate_file.exists():
                return candidate_file, next_date_str

        return None, None  # Return None if no valid file is found

    def filter_messages(messages, date, fraction):
        """
        Filters messages based on the fraction of the day and a specific date.

        Args:
            messages (list): List of messages, where each message is a tuple (timestamp, user, text).
            date (str): The date to filter messages by (format: "YYYY-MM-DD").
            fraction (float): A number between -1 and 1 indicating the fraction of the day to filter.
                              Positive values select the first part of the day, and negative values
                              select the last part of the day.

        Returns:
            list: Filtered list of messages.
        """
        if not (-1 <= fraction <= 1):
            raise ValueError("Fraction must be between -1 and 1.")

        # Ensure messages are sorted by timestamp
        messages.sort(key=lambda x: x[0])

        # Filter messages to ensure they match the specified date
        messages = [msg for msg in messages if msg[0].startswith(date)]
        if not messages:
            return []

        # Parse the date to calculate start of the day
        day_start = datetime.datetime.strptime(date, "%Y-%m-%d")

        # Calculate the time range for the fraction
        total_seconds = 24 * 60 * 60  # Total seconds in a day
        duration = abs(fraction) * total_seconds  # Duration in seconds

        if fraction > 0:
            # First part of the day
            time_start = day_start
            time_end = day_start + datetime.timedelta(seconds=duration)
        else:
            # Last part of the day
            time_end = day_start + datetime.timedelta(days=1)  # End of the day
            time_start = time_end - datetime.timedelta(seconds=duration)

        # Filter messages within the calculated time range
        filtered_messages = [
            message
            for message in messages
            if time_start
            <= datetime.datetime.strptime(message[0], "%Y-%m-%d %H:%M:%S")
            < time_end
        ]

        return filtered_messages

    search_prev = adjacent_range[0] < 0
    search_next = adjacent_range[1] > 0

    d0 = pathlib.Path(directory)

    file_this = get_filename(d0, channel, date)
    messages_this = []
    messages_prev = []
    messages_next = []

    if file_this.exists():
        messages_this = load_messages(file_this)
        print(messages_this)

        if search_prev:
            file_prev, date_prev = find_adjacent(d0, channel, date, -1)
            if file_prev and file_prev.exists():
                messages_prev = load_messages(file_prev)
                messages_prev = filter_messages(
                    messages_prev, date_prev, search_prev
                )

        if search_next:
            file_next, date_next = find_adjacent(d0, channel, date, +1)
            if file_next and file_next.exists():
                messages_next = load_messages(file_next)
                messages_next = filter_messages(
                    messages_next, date_next, search_next
                )

    return A_GIS.Code.make_struct(
        this=messages_this, next=messages_next, prev=messages_prev
    )
