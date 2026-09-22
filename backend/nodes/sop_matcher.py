import operator
from pathlib import Path

import yaml

from backend.state import WeatherBotState


SOP_FILE = Path(__file__).resolve().parents[2] / "sops" / "sops.yaml"


def load_sops() -> list:
    with open(SOP_FILE, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return data.get("sops", [])


def compare(value, op, threshold) -> bool:
    operations = {
        ">": operator.gt,
        ">=": operator.ge,
        "<": operator.lt,
        "<=": operator.le,
        "==": operator.eq,
    }

    if op not in operations:
        return False

    return operations[op](value, threshold)


def get_weather_value(weather: dict, weather_type: str):
    relevant = weather.get("relevant_weather", {})

    mapping = {
        "temperature": "temperature",
        "wind_speed": "wind_speed",
        "precipitation": "precipitation",
        "weather_code": "weather_code",
        "uv_index": "uv_index",
    }

    field = mapping.get(weather_type)

    if field:
        return relevant.get(field)

    return None


def suitable_for_activity(sop: dict, weather: dict) -> bool:
    required = sop.get("condition", {}).get("required", {})
    relevant = weather.get("relevant_weather", {})

    temperature = relevant.get("temperature")
    precipitation = relevant.get("precipitation")
    wind_speed = relevant.get("wind_speed")

    if temperature is None:
        return False

    if (
        "min_temperature" in required
        and temperature < required["min_temperature"]
    ):
        return False

    if (
        "max_temperature" in required
        and temperature > required["max_temperature"]
    ):
        return False

    if (
        "max_precipitation" in required
        and precipitation > required["max_precipitation"]
    ):
        return False

    if (
        "max_wind_speed" in required
        and wind_speed > required["max_wind_speed"]
    ):
        return False

    return True


def activity_matches(sop_activity: str, activity: str) -> bool:

    if sop_activity == activity:
        return True

    if sop_activity == "outdoor_activity":
        return True

    if activity in [
        "running",
        "cycling",
        "walking",
        "hiking",
    ]:
        return sop_activity == "outdoor_activity"

    return False


def sop_matches(
    sop: dict,
    activity: str,
    weather: dict,
) -> bool:

    if not activity_matches(
        sop.get("activity"),
        activity,
    ):
        return False

    condition = sop.get("condition", {})
    condition_type = condition.get("type")

    # Fuzzy / non-numeric policy
    if condition_type == "suitable_for_activity":
        return suitable_for_activity(
            sop,
            weather,
        )

    actual_value = get_weather_value(
        weather,
        condition_type,
    )

    if actual_value is None:
        return False

    if condition.get("operator") == "in":
        return actual_value in condition.get(
            "values",
            [],
        )

    return compare(
        actual_value,
        condition.get("operator"),
        condition.get("value"),
    )


def match_sop(state: WeatherBotState) -> dict:

    activity = state.get("activity")
    relevant_weather = state.get(
        "relevant_weather",
        {},
    )

    if not activity:
        return {
            "matched_sops": [],
            "matched_sop": None,
            "sop_match_reason": (
                "No activity was identified."
            ),
        }

    if not relevant_weather:
        return {
            "matched_sops": [],
            "matched_sop": None,
            "sop_match_reason": (
                "Relevant weather data is unavailable."
            ),
        }

    weather_context = {
        "relevant_weather": relevant_weather
    }

    sops = load_sops()

    matching_sops = []

    for sop in sops:

        if sop_matches(
            sop,
            activity,
            weather_context,
        ):
            matching_sops.append(sop)

    if not matching_sops:
        return {
            "matched_sops": [],
            "matched_sop": None,
            "sop_match_reason": (
                "No applicable SOP was found."
            ),
        }

    severity_priority = {
        "critical": 4,
        "high": 3,
        "medium": 2,
        "low": 1,
    }

    matching_sops.sort(
        key=lambda sop: severity_priority.get(
            sop.get("severity", "low"),
            0,
        ),
        reverse=True,
    )

    selected_sop = matching_sops[0]

    return {
        "matched_sops": matching_sops,
        "matched_sop": selected_sop,
        "sop_match_reason": (
            f"Selected {selected_sop['id']} "
            f"from {len(matching_sops)} matching SOP(s) "
            f"using severity priority."
        ),
    }