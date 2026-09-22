from backend.state import WeatherBotState


def error_response(state: WeatherBotState) -> dict:

    error = state.get(
        "error",
        "Unable to process the request.",
    )

    return {
        "response": (
            f"Unable to provide a weather advisory: {error}"
        )
    }


def no_sop_response(state: WeatherBotState) -> dict:

    return {
        "response": (
            "No applicable SOP was found for the "
            "requested activity and weather conditions."
        )
    }


def advisory_response(state: WeatherBotState) -> dict:

    sop = state.get("matched_sop")

    weather = state.get(
        "relevant_weather",
        {},
    )

    if not sop:

        return {
            "response": (
                "No applicable SOP was found for the "
                "requested activity and weather conditions."
            )
        }

    temperature = weather.get(
        "temperature"
    )

    wind = weather.get(
        "wind_speed"
    )

    precipitation = weather.get(
        "precipitation"
    )

    period = weather.get(
        "period",
        "current",
    )

    return {
        "response": (
            f"Weather advisory for "
            f"{state.get('activity')} in "
            f"{state.get('location')} "
            f"({period}):\n\n"

            f"Temperature: {temperature}°C\n"
            f"Wind speed: {wind} km/h\n"
            f"Precipitation: {precipitation} mm\n\n"

            f"SOP: {sop.get('id')}\n"
            f"Advice: {sop.get('advice')}\n\n"

            f"Match reason: "
            f"{state.get('sop_match_reason')}"
        )
    }