import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


# ------------------------------------------------------------
# Known Indian cities
# ------------------------------------------------------------
# These coordinates avoid ambiguous city-name results from
# the Open-Meteo geocoding API.

KNOWN_CITIES = {
    "bangalore": {
        "name": "Bengaluru",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "country": "India",
        "country_code": "IN",
        "timezone": "Asia/Kolkata",
    },
    "bengaluru": {
        "name": "Bengaluru",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "country": "India",
        "country_code": "IN",
        "timezone": "Asia/Kolkata",
    },
    "mysore": {
        "name": "Mysuru",
        "latitude": 12.2958,
        "longitude": 76.6394,
        "country": "India",
        "country_code": "IN",
        "timezone": "Asia/Kolkata",
    },
    "mysuru": {
        "name": "Mysuru",
        "latitude": 12.2958,
        "longitude": 76.6394,
        "country": "India",
        "country_code": "IN",
        "timezone": "Asia/Kolkata",
    },
    "mumbai": {
        "name": "Mumbai",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "country": "India",
        "country_code": "IN",
        "timezone": "Asia/Kolkata",
    },
    "delhi": {
        "name": "Delhi",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "country": "India",
        "country_code": "IN",
        "timezone": "Asia/Kolkata",
    },
    "hyderabad": {
        "name": "Hyderabad",
        "latitude": 17.3850,
        "longitude": 78.4867,
        "country": "India",
        "country_code": "IN",
        "timezone": "Asia/Kolkata",
    },
    "chennai": {
        "name": "Chennai",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "country": "India",
        "country_code": "IN",
        "timezone": "Asia/Kolkata",
    },
    "pune": {
        "name": "Pune",
        "latitude": 18.5204,
        "longitude": 73.8567,
        "country": "India",
        "country_code": "IN",
        "timezone": "Asia/Kolkata",
    },
    "kolkata": {
        "name": "Kolkata",
        "latitude": 22.5726,
        "longitude": 88.3639,
        "country": "India",
        "country_code": "IN",
        "timezone": "Asia/Kolkata",
    },
}


def geocode_location(location: str) -> dict:

    normalized_location = location.strip().lower()

    # --------------------------------------------------------
    # Use known coordinates first
    # --------------------------------------------------------

    if normalized_location in KNOWN_CITIES:
        return KNOWN_CITIES[normalized_location]

    # --------------------------------------------------------
    # Open-Meteo geocoding fallback
    # --------------------------------------------------------

    params = {
        "name": location,
        "count": 20,
        "language": "en",
        "format": "json",
    }

    response = requests.get(
        GEOCODING_URL,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    results = data.get("results", [])

    if not results:
        raise ValueError(
            f"Could not find location: {location}"
        )

    # Prefer Indian results when available.
    india_results = [
        result
        for result in results
        if result.get("country_code") == "IN"
    ]

    if india_results:
        result = india_results[0]
    else:
        result = results[0]

    return {
        "name": result["name"],
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "country": result.get("country"),
        "country_code": result.get("country_code"),
        "timezone": result.get("timezone"),
    }