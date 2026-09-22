from backend.state import WeatherBotState
from backend.services.geocoding import geocode_location
from backend.services.open_meteo import get_weather


def fetch_weather(state: WeatherBotState) -> dict:
    """
    Resolve the location and fetch live weather data.
    """

    location = state.get("location")

    if not location:
        return {
            "error": "No location was provided."
        }

    try:
        location_data = geocode_location(location)

        weather = get_weather(
            location_data["latitude"],
            location_data["longitude"],
        )

        return {
            "location": location_data["name"],
            "latitude": location_data["latitude"],
            "longitude": location_data["longitude"],
            "timezone": location_data.get("timezone"),
            "weather": weather,
        }

    except Exception as exc:
        return {
            "error": f"Unable to retrieve weather data: {exc}"
        }