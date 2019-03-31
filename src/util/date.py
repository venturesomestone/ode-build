# ------------------------------------------------------------- #
#                 Obliging Ode & Unsung Anthem
# ------------------------------------------------------------- #
#
# This source file is part of the Obliging Ode and Unsung Anthem
# projects.
#
# Copyright (C) 2019 Antti Kivi
# All rights reserved
#
# ------------------------------------------------------------- #

"""This support module helps to handle date and time objects."""

from datetime import datetime, time


def date_difference(first, second):
    """
    Works out the time that is left from the second date until
    the first date. The returned time is given in seconds.

    first -- the first date
    second -- the second date
    """
    d = second - first
    return d.days * 24 * 3600 + d.seconds


def to_days(s):
    """
    Turns some seconds into days, hours, minutes, seconds.

    s -- time in seconds
    """
    minutes, seconds = divmod(s, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return days, hours, minutes, seconds


def to_date_string(s):
    """
    Turns some seconds into a string of days, hours, minutes,
    seconds.

    s -- time in seconds
    """
    (days, hours, minutes, seconds) = to_days(s)

    if days == 1:
        days_str = "1 day"
    else:
        days_str = "{} days".format(days)

    if hours == 1:
        hours_str = "1 hour"
    else:
        hours_str = "{} hours".format(hours)

    if minutes == 1:
        minutes_str = "1 minute"
    else:
        minutes_str = "{} minutes".format(minutes)

    if seconds == 1:
        seconds_str = "1 second"
    else:
        seconds_str = "{} seconds".format(seconds)

    return "{}, {}, {}, and {}".format(
        days_str, hours_str, minutes_str, seconds_str)
