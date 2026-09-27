# Lesson 25.1: Geo Search

## Motto
"Earth is a sphere, not a flat plane: geo search uses spatial BKD trees and Haversine distance."

## Problem
In mobile delivery apps and local store finders, users search for: *"coffee shops within 2 kilometers of my current latitude and longitude"*. Naive SQL bounding boxes do not account for Earth's curvature or circular radii.

## Prediction
Will a rectangular bounding box query return stores that are in the corners of the box but farther than 2 km from the center?

## Why this matters
Elasticsearch indexes `geo_point` fields using 2-dimensional BKD trees (spatial points) for spatial bounding boxes and radial distance filters.

## First principles
* **`geo_point`:** Latitude and Longitude pair: `{"lat": 40.7128, "lon": -74.0060}`.
* **Haversine Formula:** Calculates great-circle distance between two points on a sphere of radius $R$:
  $$d = 2R rcsin\left(\sqrt{\sin^2\left(rac{\Delta\phi}{2}ight) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(rac{\Delta\lambda}{2}ight)}ight)$$

## Mental model
```text
      ┌─────────────────────────┐
      │   Corner (Distance > R) │
      │      ┌───────────┐      │
      │      │  RADIUS   │      │
      │      │    (R)    │      │
      │      └───────────┘      │
      │  Bounding Box Rectangle │
      └─────────────────────────┘
  Geo-Distance enforces circular radius; Bounding Box is faster rectangular filter.
```

## Build it
See `code/haversine_distance.py` calculating spatial distances and radial filters in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/25-geo-search/experiments/run_experiment.sh
```

## Inspect it
Create an index with `geo_point` mapping and execute a `geo_distance` query:
```bash
curl -X POST http://localhost:9200/stores/_search -H "Content-Type: application/json" -d '{
  "query": {
    "bool": {
      "filter": {
        "geo_distance": {
          "distance": "5km",
          "location": { "lat": 37.7749, "lon": -122.4194 }
        }
      }
    }
  }
}'
```

## Measure it
Measure query latency comparing `geo_bounding_box` (simple coordinate checks) vs `geo_distance` (trigonometric calculations).

## Break it
Swap latitude and longitude values: latitude must be between $-90$ and $+90$; longitude between $-180$ and $+180$. Elasticsearch rejects invalid ranges with `illegal_argument_exception`.

## Recover it
Follow the GeoJSON standard: `[lon, lat]` in arrays, or explicit `{"lat": ..., "lon": ...}` in objects.

## Modify it
Sort results by distance from user location: `sort: [{ "_geo_distance": { "location": ... } }]`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does `geo_bounding_box` execute faster than `geo_distance`?
2. What coordinate order does Elasticsearch expect when geo points are provided as an array?

## Guarantees
* Provides accurate spherical distance calculations across the globe.

## Non-guarantees
* Does not compute street navigation routing distance or traffic conditions.

## When to use this
* Store locators, ride sharing, delivery radius, and spatial analytics.

## When not to use this
* Complex multi-polygon GIS spatial topology operations (use PostGIS for complex GIS).

## What comes next
In Phase 26, we begin the next major milestone: Aggregations and Analytics From First Principles.
