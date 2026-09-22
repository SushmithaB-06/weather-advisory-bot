from backend.state import WeatherBotState


def select_weather_period(state: WeatherBotState) -> dict:
    weather = state.get("weather", {})
    time_reference = state.get("time_reference", "today")

    current = weather.get("current", {})
    hourly = weather.get("hourly", {})
    daily = weather.get("daily", {})

    # Default: current weather
    relevant_weather = {
        "period": "current",
        "temperature": current.get("temperature_2m"),
        "wind_speed": current.get("wind_speed_10m"),
        "precipitation": current.get("precipitation"),
        "weather_code": current.get("weather_code"),
        "uv_index": current.get("uv_index"),
    }

    # Tomorrow
    if time_reference == "tomorrow":
        if daily.get("temperature_2m_max"):
            relevant_weather = {
                "period": "tomorrow",
                "temperature": daily["temperature_2m_max"][1],
                "wind_speed": daily["wind_speed_10m_max"][1],
                "precipitation": daily["precipitation_sum"][1],
                "weather_code": daily["weather_code"][1],
                "uv_index": daily["uv_index_max"][1],
            }

    # Evening / afternoon / morning
    elif time_reference in [
        "this evening",
        "tonight",
        "this afternoon",
        "morning",
    ]:

        times = hourly.get("time", [])
        temperatures = hourly.get("temperature_2m", [])
        winds = hourly.get("wind_speed_10m", [])
        precipitation = hourly.get("precipitation", [])
        weather_codes = hourly.get("weather_code", [])
        uv_indexes = hourly.get("uv_index", [])

        selected_indexes = []

        for i, time in enumerate(times):
            hour = int(time[11:13])

            if time_reference in ["this evening", "tonight"]:
                if 18 <= hour <= 22:
                    selected_indexes.append(i)

            elif time_reference == "this afternoon":
                if 12 <= hour <= 17:
                    selected_indexes.append(i)

            elif time_reference == "morning":
                if 6 <= hour <= 11:
                    selected_indexes.append(i)

        if selected_indexes:
            i = selected_indexes[0]

            relevant_weather = {
                "period": time_reference,
                "temperature": temperatures[i],
                "wind_speed": winds[i],
                "precipitation": precipitation[i],
                "weather_code": weather_codes[i],
                "uv_index": uv_indexes[i],
            }

    return {
        "relevant_weather": relevant_weather
    }