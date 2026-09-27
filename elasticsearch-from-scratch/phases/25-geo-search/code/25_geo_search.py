#!/usr/bin/env python3
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

if __name__ == "__main__":
    # San Francisco coords
    user_lat, user_lon = 37.7749, -122.4194
    stores = [
        {"name": "Downtown SF Store", "lat": 37.7833, "lon": -122.4167},
        {"name": "Oakland Store", "lat": 37.8044, "lon": -122.2712},
        {"name": "San Jose Store", "lat": 37.3382, "lon": -121.8863}
    ]
    print(f"User location: ({user_lat}, {user_lon})\n")
    for s in stores:
        dist = haversine(user_lat, user_lon, s["lat"], s["lon"])
        within_15km = dist <= 15.0
        print(f"Store: {s['name']:20s} | Distance: {dist:6.2f} km | Within 15km: {within_15km}")
