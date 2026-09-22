from typing import TypedDict


class WeatherBotState(TypedDict, total=False):

    # Current user message
    user_message: str

    # Session context
    previous_location: str
    previous_activity: str

    # Location
    location: str
    latitude: float
    longitude: float
    timezone: str

    # Intent
    activity: str
    intent: str
    time_reference: str

    # Weather
    weather: dict
    relevant_weather: dict

    # SOP
    matched_sops: list
    matched_sop: dict
    sop_match_reason: str

    # Final response
    response: str

    # Errors
    error: str