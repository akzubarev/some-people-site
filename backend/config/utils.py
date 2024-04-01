import requests


def get_location_from_ip(ip):
    GEOLOCATION_SERVICE_URL = "http://daemon.echoip:8080/"
    ip_data = requests.get(f"{GEOLOCATION_SERVICE_URL}json?ip={ip}",
                           verify=False).json()
    return {
        "country": ip_data.get("country", None),
        "country_iso": ip_data.get("country_iso", None),
        "city": ip_data.get("city", None),
        "longitude": ip_data.get("longitude", None),
        "latitude": ip_data.get("latitude", None),
    }
