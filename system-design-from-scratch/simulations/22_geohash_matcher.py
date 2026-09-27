import math
from typing import List, Tuple

class SpatialGridMatcher:
    def __init__(self, grid_size_deg: float = 0.05):
        self.grid_size = grid_size_deg
        self.drivers: List[Tuple[str, float, float]] = []

    def add_driver(self, driver_id: str, lat: float, lng: float):
        self.drivers.append((driver_id, lat, lng))

    def find_nearby(self, lat: float, lng: float, radius_km: float = 5.0) -> List[str]:
        # Rough distance approximation: 1 deg lat ~ 111 km
        res = []
        for did, dlat, dlng in self.drivers:
            dist = math.sqrt(((dlat - lat) * 111)**2 + ((dlng - lng) * 111)**2)
            if dist <= radius_km:
                res.append(did)
        return res
