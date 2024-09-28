"""Dates handling utils."""
from datetime import date, datetime

from django.utils import timezone


def date_to_datetime(day: date, end=False):
    """Converts a date to a datetime object."""
    time = datetime.min.time() if end is False else datetime.max.time()
    return timezone.make_aware(datetime.combine(date=day, time=time))


def day_range(day: date = date.today()):
    """Converts a date to a range from 00 to 23:59."""
    day_start = date_to_datetime(day)
    day_end = date_to_datetime(day, end=True)
    return day_start, day_end
