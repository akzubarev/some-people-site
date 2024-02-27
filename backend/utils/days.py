from datetime import datetime, date, timedelta
from django.utils import timezone


def date_to_datetime(day: date, end=False):
    time = datetime.min.time() if end is False else datetime.max.time()
    return timezone.make_aware(datetime.combine(date=day, time=time))


def day_range(day: date = date.today()):
    day_start = date_to_datetime(day)
    day_end = date_to_datetime(day, end=True)
    return day_start, day_end


def month_start():
    now = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return now - timedelta(days=now.day - 1)
