"""
Resilient, production-ready solution for lab-24-unhandled-timezone-dst-shift-in-grain.
"""
import datetime
def get_utc_hourly_key():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:00Z")
