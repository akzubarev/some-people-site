import os
import sys
import time
import datetime

import django

sys.path[0] += '/../..'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.users.models import User
from backend.utils import get_location_from_ip
from django.core.cache import cache
from rest_framework_tracking.models import APIRequestLog
from django.utils import timezone
from django.db.models import Q, Count, F, Sum


if __name__ == "__main__":
    sleep_interval = 60 * 60
    while True:
        start = timezone.now()
        orig_start = start
        timings = []

        cache.set("num_of_visits", APIRequestLog.objects.filter(path="/api/users/me/").count() // 10, None) # avg 10 requests per page :^)
        timings.append({"title": "Number of visits", "sec": timezone.now() - start})
        start = timezone.now()

        all_cities_with_visits = []
        cached_locations = []

        print(APIRequestLog.objects.distinct('remote_addr').count())
        for ip in APIRequestLog.objects.distinct('remote_addr').values_list('remote_addr', flat=True):
            location = get_location_from_ip(ip)
            # if f"{location['latitude']}:{location['longitude']}" not in cached_locations:
            if f"{location['country_iso']}:{location['city']}" not in cached_locations:
                all_cities_with_visits.append({
                    "city": location["city"],
                    "country_iso": location["country_iso"],
                    "lat": location["latitude"],
                    "long": location["longitude"],
                    })
                cached_locations.append(f"{location['country_iso']}:{location['city']}")
        cache.set("all_cities_visits", all_cities_with_visits, None)

        timings.append({"title": "All cities visits", "sec": timezone.now() - start})
        start = timezone.now()

        # Оказалось что и без кэша быстро работает, но оставлю тут чтобы было в случае чего
        # cache.set("last_half_hour_sessions", list(
        #     APIRequestLog.objects
        #     .exclude(user__city__isnull=True)
        #     .filter(requested_at__gte=timezone.now() - datetime.timedelta(minutes=30))
        #     .annotate(
        #         city=F('user__city'), lat=F('user__lat'), long=F('user__long'), country_iso=F('user__country_iso'))
        #     .distinct('city')
        #     .values('city', 'lat', 'long', 'country_iso', 'requested_at')
        #     # .count()
        #           ))
        # timings.append({"title": "Half hour sessions cities", "sec": timezone.now() - start})
        # start = timezone.now()

        # cache.set("cities_with_users", list(
        #     User.objects
        #     .filter(country_iso__isnull=False)
        #     .values('city', 'country_iso', 'lat', 'long')
        #     .annotate(partners=Count('id'))
        #           ))
        # timings.append({"title": "Cities with users", "sec": timezone.now() - start})
        # start = timezone.now()

        timings.append({"title": "All", "sec": timezone.now() - orig_start})

        print("Number of visits:", cache.get("num_of_visits"))
        print("Number of all cities visits:", len(cache.get("all_cities_visits")))
        # print("Number of cities from last 30 mins:", len(cache.get("last_half_hour_sessions")))
        # print("Cities with users:", len(cache.get("cities_with_users")))
        print()

        for t in timings:
            print(f"{t['title']} gathered in {t['sec'].total_seconds():.2f} sec")

        print(f"Next update scheduled at {timezone.now() + datetime.timedelta(seconds=sleep_interval)}")
        time.sleep(sleep_interval)
