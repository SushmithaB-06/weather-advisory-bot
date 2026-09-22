import requests

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(latitude: float, longitude: float) -> dict:
    params = {
        "latitude": latitude,
        "longitude": longitude,

        "current": ",".join([
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "weather_code",
            "wind_speed_10m",
            "uv_index",
        ]),

        "hourly": ",".join([
            "temperature_2m",
            "precipitation",
            "precipitation_probability",
            "weather_code",
            "wind_speed_10m",
            "uv_index",
        ]),

        "daily": ",".join([
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "precipitation_probability_max",
            "weather_code",
            "wind_speed_10m_max",
            "uv_index_max",
        ]),

        "forecast_days": 3,
        "timezone": "auto",
    }

    response = requests.get(
        WEATHER_URL,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()