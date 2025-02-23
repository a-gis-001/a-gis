"""Manage the 'when' of everything.

Time data is necessary to understand progress and relationships.

Without time, we cannot fully understand arbitrary data and the
events described.

The main output of all functions in this module should be a best-estimate time
and a possible time range. A range is a distribution. For example, converting
1971 to a best-estimate time could be January 1, 1971 or July 15, 1971. If the
time-range is January 1 to December 31, then the July option is probably better.

This module also manages "events". Events occur at specific times and
there may be constraints that allow events to be ordered, i.e.
time(event1)>time(event0) with some confidence. These constraints can
be multiple.

For example, if the two events are a purchase and the delivery arriving:

- time(purchase) = 2024
- time(delivery) = November 2024
- time(delivery) - time(purchase) > 0 [100%]
- time(delivery) - time(purchase) > 1 week [95%]
- time(delivery) - time(purchase) < 1 week [5%]
- time(delivery) - time(purchase) = TruncatedNormalDistribution(2 weeks)

This data can be used to piece together the events to determine the most likely
times that things happened.
"""
# Functions
from .convert_to_datetime import convert_to_datetime
from .convert_to_string import convert_to_string
from .get import get
