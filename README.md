# Supercivilian API Documentation

## Overview

This API helps users find nearby shelters by combining Google Places API for location search and ArcGIS for shelter data. The API provides a seamless flow from searching for a location to finding nearby shelters.

## API Endpoints

### Google Places Endpoints

| Endpoint                          | Description                                     |
| --------------------------------- | ----------------------------------------------- |
| `GET /google/search/autocomplete` | Search for places with autocomplete suggestions |
| `GET /google/place/<str:id>`      | Get detailed information about a specific place |

### Shelter Endpoints

| Endpoint                        | Description                                       |
| ------------------------------- | ------------------------------------------------- |
| `GET /arcgis/shelters`          | Find shelters near a geographic point             |
| `GET /arcgis/shelters/<int:id>` | Get detailed information about a specific shelter |

## Usage Flow

1. **Location Search**
   - Send user's input to `/google/search/autocomplete?query={search_term}`
   - User selects from the returned location suggestions

2. **Get Location Details**
   - Use selected location's `place_id` to fetch details via `/google/place/{place_id}`
   - Extract coordinates (`latitude` and `longitude`)

3. **Find Nearby Shelters**
   - Query `/arcgis/shelters?latitude={lat}&longitude={lon}`
   - Optionally filter results using query parameters (see Parameters section)

4. **Get Shelter Details**
   - Use shelter's `id` to fetch complete details via `/arcgis/shelters/{id}`

## Parameters

### Search Autocomplete

- `query` (required): Text to search for (e.g., "Warsaw")

### Shelter Search

- `latitude` (required): Geographic latitude
- `longitude` (required): Geographic longitude
- `range` (optional): Search radius in meters (default: 30000)
- `limit` (optional): Maximum number of results (default: 10)
- `offset` (optional): Offset of the results (default: 0)

## Response Formats

### Location Search Response

```json
{
    "success": true,
    "payload": [
        {
            "place_id": "ChIJAZ-GmmbMHkcR_NPqiCq-8HI",
            "description": "Warszawa, Polska",
            "types": ["locality", "political", "geocode"]
        }
        // ... more results
    ]
}
```

### Place Details Response

```json
{
    "success": true,
    "payload": {
        "id": "ChIJAZ-GmmbMHkcR_NPqiCq-8HI",
        "latitude": 52.2296756,
        "longitude": 21.0122287,
        "name": "Warszawa",
        "formatted_address": "Warszawa, Polska",
        "website": "http://www.um.warszawa.pl/"
    }
}
```

### Shelter List Response

```json
{
    "success": true,
    "payload": [
        {
            "id": 215542,
            "longitude": 21.0117278584427,
            "latitude": 52.2298239083584,
            "inventory_type": "[1] - Ropoznanie operacyjne",
            "access_type": "[1] - droga pożarowa",
            "area": 5000,
            "capacity": 3333,
            "quality": 8,
            "category": "[3] - MDS",
            "purpose": "[1] - M",
            "address": "Marszałkowska - Al. Jerozolimskie, 00-693 Warszawa",
            "distance": 37.99  // distance in meters from search point
        }
        // ... more results
    ]
}
```

These results are sorted by distance from the search point.

## Error Handling

All endpoints return a consistent error format:
```json
{
    "success": false,
    "error": {
        "message": "Human readable error message"
    }
}
```

## ArcGIS API Documentation

You can find our documentation for the ArcGIS API [here](docs/arcgis.md).
