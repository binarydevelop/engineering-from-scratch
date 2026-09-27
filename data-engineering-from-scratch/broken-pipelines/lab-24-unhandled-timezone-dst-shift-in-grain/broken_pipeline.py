"""
Broken implementation demonstrating the flaw in lab-24-unhandled-timezone-dst-shift-in-grain.
"""
import datetime
def get_naive_hourly_key():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:00") # Ambiguous on DST
